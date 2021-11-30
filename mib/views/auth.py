from flask import Blueprint, redirect, render_template, abort
from flask_login import login_user, logout_user
from mib.swagger_client.models.user import User

from mib.database import db
from mib.forms import LoginForm
from mib.views.doc import auto

auth = Blueprint('auth', __name__)


# noinspection PyUnresolvedReferences
@auth.route('/login', methods=['GET', 'POST'])
@auto.doc(groups=['routes'])
def login():
    """
    Login functionality based upon flask_logins

    :return: a rendered view
    """
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        if UserManager.authenticate(email, password):
            user = UserManager.get_by_mail(email)
            user = User.from_dict(user)
            login_user(user)
            return redirect('/')
        else:
            abort(401)
    return render_template('login.html', form=form)


@auth.route("/logout")
@auto.doc(groups=['routes'])
def logout():
    """
    Logout functionality

    :return: a rendered view
    """
    logout_user()
    return redirect('/')
