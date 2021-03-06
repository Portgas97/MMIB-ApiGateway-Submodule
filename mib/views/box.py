from flask import Blueprint, abort, redirect, request
from flask.templating import render_template
from flask_login import login_required, current_user

from mib.forms import ForwardForm, ReplyForm
from mib.send import send_messages, save_draft
from mib.views.doc import auto
from mib.rao.notifications_manager import NotificationsManager as nm
from mib.rao.message_manager import MessageManager as mm
from mib.rao.user_manager import UserManager as um

box = Blueprint('box', __name__)


# noinspection PyUnresolvedReferences
@box.route("/drafts", methods=["GET"], defaults={'_id': None})
@box.route("/drafts/<_id>", methods=["GET", "DELETE"])
@auto.doc(groups=['routes'])
@login_required
def prep_drafts(_id):
    """
    Queries the message microservice and prepares the view
    had accessed the inbox functionality
    We lack the API call to query a single message for security reasons

    :param _id: optional message id
    :return: a rendered view
    """
    user_mail = current_user.email
    role = 'drafts'
    messages = mm.get_box(user_mail, role)
    return display_box(messages, role, _id)


# noinspection PyUnresolvedReferences
@box.route("/inbox", methods=["GET"], defaults={'_id': None})
@box.route("/inbox/<_id>", methods=["GET", "DELETE"])
@auto.doc(groups=['routes'])
@login_required
def prep_inbox(_id):
    """
    Queries the message microservice and prepares the view
    had accessed the inbox functionality
    We lack the API call to query a single message for security reasons

    :param _id: optional message id
    :return: a rendered view
    """
    user_mail = current_user.email
    role = 'inbox'
    messages = mm.get_box(user_mail, role)
    return display_box(messages, role, _id)


@box.route("/outbox", methods=["GET"], defaults={'_id': None})
@box.route("/outbox/<_id>", methods=["GET", "DELETE"])
@auto.doc(groups=['routes'])
@login_required
def prep_outbox(_id):
    """
    Prepares the query arguments to populate the message list as if the user
    had accessed the sent messages functionality
    If the optional message id is passed, the query will return only the
    specific message with that id
    Performs all necessary checks to make sure the user is authorized to view
    a specific message

    :param _id: optional message id
    :return: a list of sent messages, divided in delivered and pending
    """
    user_mail = current_user.email
    role = 'outbox'
    messages = mm.get_box(user_mail, role)
    return display_box(messages, role, _id)


def display_box(messages, role, optional_id):
    """
        returns either the inbox or the outbox, based on the route that was called
        then performs a database query with the prepared arguments for that route
        finally renders everything in a proper page
        works for both a single message and a list of messages
        DELETE will only delete the message for the current user, not their partner

        :param messages: list of message json elements
        :param role: either inbox or outbox depending on the route
        :param optional_id: id of the specific message to render
        :return: a rendered view
        """
    if optional_id is not None:
        # single message box
        # display a view of only that message
        for message in messages:
            if int(message['id']) == int(optional_id):
                if request.method == "DELETE":
                    if role == 'inbox' or role == 'outbox':
                        if message['status'] == 2:
                            mm.delete_message(current_user.email, optional_id)
                        elif message['status'] == 1:
                            withdraw(optional_id)
                        else:
                            abort(400)
                    elif role == 'drafts':
                        mm.delete_draft(optional_id)
                    return redirect("/" + role)
                if role == 'inbox':
                    if not message['is_read']:
                        notify_sender(int(optional_id), message)
                        mm.set_as_read(optional_id)
                return render_template(
                    'list/box_one.html',
                    message=message,
                    role=role
                )
        return redirect("/" + role)
    else:
        # multi-message box
        sent_messages = []
        pending_messages = None
        if role == 'outbox':
            pending_messages = []
            for message in messages:
                if message['status'] == 1:
                    pending_messages.append(message)
                elif message['status'] == 2:
                    sent_messages.append(message)
            messages = sent_messages
        return render_template(
            'list/box.html',
            messages=messages,
            pending=pending_messages,
            role=role
        )


def notify_sender(id, message):
    """
    notifies the sender when the receiver opens for the first time a message

    :param id: the id of the viewed message
    :param message: message json object
    """
    title = message['receiver_mail'] + " Read Your Message"
    description = \
        "<i>" + "\"" + message['message'] + "\"" + "</i>"
    nm.create_notification(
        message['sender_mail'],
        title,
        description,
        message['time'],
        id
    )
    return


@box.route("/inbox/forward/<m_id>", methods=["GET", "POST"])
@auto.doc(groups=['routes'])
@login_required
def forward(m_id):
    """
    Implements the forward message feature.

    :param m_id: message id
    :return: a rendered view
    """
    if m_id is not None:
        # get the message from the microservice
        messages = mm.get_box(current_user.email, 'inbox')
        for message in messages:
            if int(message['id']) == int(m_id):
                form = ForwardForm()
                if form.validate_on_submit():
                    address = form.data["recipient"]
                    time = form.data["time"]
                    # add a forward header to the message
                    frw_message = "Forwarded by: " + message['receiver_mail']
                    frw_message += "\nFrom: " + message['sender_mail']
                    frw_message += "\n\n" + message['message']
                    if message['image'] != "":
                        image = message['image']
                        image_hash = message['image_hash']
                    else:
                        image = None
                        image_hash = None
                    correctly_sent, not_correctly_sent = send_messages(
                        address.split(', '), current_user.email, time,
                        frw_message, image, image_hash)
                    return render_template(
                        'done_sending.html',
                        users1=correctly_sent,
                        users2=not_correctly_sent,
                        text=frw_message
                    )
                return render_template('request_form.html', form=form)
        abort(404)


@box.route("/outbox/withdraw/<m_id>", methods=["GET"])
@auto.doc(groups=['routes'])
@login_required
def withdraw(m_id):
    """
    Implements the withdraw message feature.
    The user can spend lottery points to withdraw a message.

    :param m_id: message id
    :return: a rendered view
    """
    if m_id is not None:
        # get the user's total lottery points

        if um.decr_points(current_user.get_id()):
            # get the message from the database
            if mm.withdraw(m_id):
                nm.delete_notification(m_id)
                return redirect('/outbox')
    abort(401)


@box.route("/inbox/reply/<m_id>", methods=["GET", "POST"])
@auto.doc(groups=['routes'])
@login_required
def reply(m_id):
    """
    Implements the reply message feature.

    :param m_id: message id
    :return: a rendered view
    """
    if m_id is None:
        return redirect('/inbox')
    messages = mm.get_box(current_user.email, 'inbox')
    for message in messages:
        if int(message['id']) == int(m_id):
            # get the receiver mail from the original message
            receiver = message['sender_mail']
            # ask the user to insert the reply text and delivery date
            form = ReplyForm()
            # send the reply
            filename = message['image']
            encoded_image = message['image_hash']
            if request.method == 'POST':
                if form.validate_on_submit():
                    message = form.data['message']
                    time = form.data['time']
                    to_parse = receiver.split(', ')
                    current_user_mail = getattr(current_user, 'email')
                    if request.form.get("save_button"):
                        # the user asked to save this message
                        save_draft(None, current_user_mail, receiver, message,
                                   time, filename, encoded_image)
                        return redirect('/')
                    correctly_sent, not_correctly_sent = send_messages(
                        to_parse, current_user_mail, time, message, None, None)
                else:
                    return render_template('error_template.html', form=form)
                return render_template(
                    'done_sending.html',
                    users1=correctly_sent,
                    users2=not_correctly_sent,
                    text=message
                )
            else:
                return render_template('send.html', form=form, use='reply')
