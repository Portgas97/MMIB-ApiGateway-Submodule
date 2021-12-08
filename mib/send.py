import pytz

from mib.rao.message_manager import MessageManager as mm
from mib.rao.user_manager import UserManager as um
from mib.rao.notifications_manager import NotificationsManager as nm


def send_messages(to_parse, current_user_mail, time, message, filename,
                  image_base64):
    """
    Enqueues a message with celery performing checks on the sender/receiver
    Saves any file it gets to a folder specific to that sender

    :param image_base64: base64 encoded image
    :param to_parse: list of mail recipient addresses, comma separated
    :param current_user_mail: mail of sender
    :param time: time of delivery, cannot be in the past
    :param message: the actual message, max size of 1024 char
    :param filename: filename of the image to save, default None
    :return: correctly_sent: list of mail addresses to which the message was
    correctly sent, including messages which blacklist the sender
    :return: not_correctly_sent: list of mail addresses which were not real
    users or were the sender themselves
    """
    correctly_sent = []
    requested_addresses = []
    not_correctly_sent = []
    valid = ""
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    for address in to_parse:
        address = address.strip()
        if um.exist_by_mail(address) and not address == current_user_mail:
            # add address to list of valid addresses string and array
            valid = valid + address + ", "
            requested_addresses.append(address)
        else:
            if address == current_user_mail:
                address = address + " (You)"
            not_correctly_sent.append(address)
    if len(valid) > 2:
        valid = valid[:-2]
        # call the multi-user send method
        array_of_replies = mm.create_message(message, current_user_mail, valid,
                                             time, filename, image_base64)
        for i in range(len(array_of_replies)):
            # we use an index rather than an iterator to advance both arrays
            # one of them is the reply array from the microservice
            # the other is the list of all addresses which were queried
            reply = array_of_replies[i]
            current_address = requested_addresses[i]
            if reply == -3:
                # abort, bad time format
                return [-3], [-3]
            if reply != -1:
                correctly_sent.append(current_address)
            if reply != -2:
                # if the user wasn't blacklisted, we create a notification
                title = current_user_mail + " Sent You a Message"
                description = "Check your <a href=\"/inbox\">Inbox</a> to " \
                              "open it."
                nm.create_notification(current_address, title,
                                       description, time, reply)
            else:
                not_correctly_sent.append(current_address)
    return correctly_sent, not_correctly_sent


def save_draft(id, current_user_mail, recipients, msg, time, image,
               image_hash):
    """
    saves a message with status of draft to the database

    :param image_hash: base64 encoding of image to save, default None
    :param image: filename of the image, default None
    :param id: id of draft to edit, default None
    :param current_user_mail: mail of sender
    :param time: time of delivery, cannot be in the past
    :param recipients: string containing the unparsed list of recipients
    :param msg: the actual message, max size of 1024 char
    """
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    if id is None:
        return mm.create_draft(
            msg,
            current_user_mail,
            recipients,
            time,
            image,
            image_hash
        )
    else:
        return mm.edit_draft(
            id,
            msg,
            current_user_mail,
            recipients,
            time,
            image,
            image_hash
        )
