from flask import Blueprint, render_template
from flask_login import current_user
from mib.views.alerts import get_notifications_count
from mib.views.doc import auto

home = Blueprint('home', __name__)



@home.route('/')
@auto.doc(groups=['routes'])
def index():
    """
    Homepage view

    :return: a rendered view
    """
    if current_user is not None and hasattr(current_user, 'id'):
        current_user_email = current_user.email
        notifications_count = get_notifications_count(current_user_email)
    else:
        notifications_count = 0

    return render_template("index.html", notifications=notifications_count)
