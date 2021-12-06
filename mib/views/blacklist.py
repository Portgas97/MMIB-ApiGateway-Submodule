import flask_login
from flask import Blueprint, redirect, render_template
from flask_login import login_required

from mib.blacklist import add2blacklist_local
from mib.database import db, Blacklist
from mib.forms import EmailForm
from mib.views.doc import auto
from mib.rao.message_manager import MessageManager as mm

blacklist = Blueprint('blacklist', __name__)


@blacklist.route('/blacklist', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def get_blacklist():
    """
    Get the logged user's blacklist.
    Only logged users are authorized to use this function.

    :return: display the user's blacklist using the blacklist template.
    """
    # get the current user
    user = flask_login.current_user
    # get the user's blacklist fom the database
    _blacklist = mm.get_blacklist()
    _blacklist = [e.email for e in _blacklist]
    return render_template('blacklist.html', result=_blacklist)


@blacklist.route('/blacklist/add', methods=['GET', 'POST'])
@auto.doc(groups=['routes'])
@login_required
def add2blacklist():
    """
    The logged user adds an email to his blacklist.
    Only logged users are authorized to use this function.

    :return: display the user's blacklist using the blacklist template or
    a form to request an email to the user.
    """
    form = EmailForm()
    if form.validate_on_submit():
        # get the email to block
        email = form.data['email']
        # get the current user
        user = flask_login.current_user
        mm.add_blacklist(user, email)
        return redirect('/blacklist')

    return render_template('request_form.html', form=form)


@blacklist.route('/blacklist/remove', methods=['GET', 'POST'])
@auto.doc(groups=['routes'])
@login_required
def delete_from_blacklist():
    """
    The logged user removes an email from his blacklist.
    Only logged users are authorized to use this function.

    :return: display the user's blacklist using the blacklist template or
    a form to request an email to the user.
    """
    form = EmailForm()
    if form.validate_on_submit():
        # get the email to block
        email = form.data['email']

        # get the current user
        user = flask_login.current_user

        # remove the email from the blacklist
        mm.remove_blacklist(user.get_email())
        return redirect('/blacklist')

    return render_template('request_form.html', form=form)
