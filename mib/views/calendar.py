from flask import Blueprint, render_template
from flask_login import login_required, current_user

from mib.views.doc import auto
from mib.rao.message_manager import MessageManager as mm


calendar = Blueprint('calendar', __name__)


def get_sent_messages(user):
    """
    :param user: the user for which to fetch messages
    :return: query of all messages sent from this user and already received
    :rtype: SQLAlchemy.session.query
    """
    role = 'outbox'
    messages = mm.get_box(user, role)
    sent_messages = []
    for message in messages:
        if message['status'] == 2:
            sent_messages.append(message)
    return sent_messages


def get_received_messages(user):
    """
    :param user: the user for which to fetch messages
    :return: query of all messages received from this user
    :rtype: SQLAlchemy.session.query
    """
    role = 'inbox'
    messages = mm.get_box(user, role)
    received_messages = []
    for message in messages:
        if message['status'] == 2:
            received_messages.append(message)
    return received_messages


@calendar.route('/calendar', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def get_calendar():
    """
    Displays messages in a calendar

    :return: a rendered view
    """
    user_email = current_user.email
    user_sent_messages = get_sent_messages(user_email)
    user_received_messages = get_received_messages(user_email)

    return render_template('calendar.html',
                           sent_messages=user_sent_messages,
                           received_messages=user_received_messages)


@calendar.route('/calendar/sent', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def get_calendar_sent():
    """
    Calendar view for sent messages only

    :return: a rendered view
    """
    user_email = current_user.email
    user_sent_messages = get_sent_messages(user_email)

    return render_template('calendar.html', sent_messages=user_sent_messages)


@calendar.route('/calendar/received', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def get_calendar_received():
    """
    Calendar view for received messages only

    :return: a rendered view
    """
    user_email = current_user.email
    user_received_messages = get_received_messages(user_email)

    return render_template('calendar.html',
                           received_messages=user_received_messages)
