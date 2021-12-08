import flask_login
from flask import Blueprint, redirect, render_template, request
from flask_login import login_required

from mib.forms import UserForm
from mib.rao.user_manager import UserManager
from mib.views.doc import auto

users = Blueprint('users', __name__)



@users.route('/users')
@auto.doc(groups=['routes'])
def _users():
    """
    Displays a list of all users by first and last name

    :return: a rendered view
    """
    users_query = UserManager.get_users_list()
    return render_template("users.html", users=users_query)



@users.route('/create_user', methods=['POST', 'GET'])
@auto.doc(groups=['routes'])
def create_user():
    """
    Registration view from which new users can enroll to the system
    in doing so it modifies the database

    :return: a rendered view
    :raises: :class:`RuntimeError`:impossible conditions
    """
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            date = form.data['date_of_birth'].strftime('%d/%m/%Y')
            if UserManager.create_user(form.data['email'],
                                       form.data['firstname'],
                                       form.data['lastname'],
                                       date,
                                       form.data['password']):
                return redirect('/users')
            else:
                form.email.errors.append("Mail already in use.")
                return render_template('error_template.html', form=form)
        else:
            return render_template('error_template.html', form=form)
    elif request.method == 'GET':
        return render_template('create_user.html', form=form)
    else:
        raise RuntimeError('This should not happen!')


def _user_data2dict(data):
    """
    Convert user data into a dictionary for easy display.

    :param data: input User object
    :returns: a dictionary containing user data
    :rtype: dict
    """
    return {
        "first name": data['firstname'],
        "last name": data['lastname'],
        "email": data['email'],
        "date of birth": data['date_of_birth'],
        "lottery points": str(data['points'])
    }


@users.route('/user_data', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def user_data():
    """
    The user can read his account's data.
    Only logged users are authorized to use this function.

    :returns: display the user's data using the user_data template.
    :rtype: View
    """
    # get the current user
    user = flask_login.current_user
    # get the user's data fom the database
    data = UserManager.get_by_id(user.id)
    # convert user data into a dictionary for easy display.
    result = _user_data2dict(data)
    return render_template('user_data.html', result=result)
