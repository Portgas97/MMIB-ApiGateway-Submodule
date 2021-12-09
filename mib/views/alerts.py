from flask import Blueprint, render_template
import flask_login
from flask_login.utils import login_required
from mib.views.doc import auto
from mib.rao.notifications_manager import NotificationsManager


alerts = Blueprint('alerts', __name__)


@alerts.route('/notifications', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def notifications():
    """
    Displays the currently pending user notifications

    :return: a rendered view
    """

    
    current_user = flask_login.current_user
    current_user_email = current_user.email

    query_notifications = NotificationsManager.get_notifications(current_user_email)
    NotificationsManager.set_notifications_as_read(current_user_email)

    return render_template("notifications.html",
                           notifications=query_notifications)


def get_notifications_count(user_email):
    """
    :param user_email: the mail we want notification count for
    :return: the number of unread notifications for user_email
    """

    notifications_count = NotificationsManager.notifications_count(user_email)
    return notifications_count
