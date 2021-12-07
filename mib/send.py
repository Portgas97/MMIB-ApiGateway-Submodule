import pytz

from mib.rao.message_manager import MessageManager as mm
from mib.rao.user_manager import UserManager as um


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
    not_correctly_sent = []
    time_aware = pytz.timezone('Europe/Rome').localize(time)
    for address in to_parse:
        address = address.strip()
        if um.exist_by_mail(address) and not address == current_user_mail:
            if mm.create_message(message, current_user_mail, address,
                                 time_aware, filename, image_base64):
                correctly_sent.append(address)
            else:
                not_correctly_sent.append(address)
        else:
            if address == current_user_mail:
                address = address + " (You)"
            not_correctly_sent.append(address)
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
