from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user

from mib.forms import CredentialsForm
from mib.database import db, User
from mib.views.doc import auto
from mib.rao.user_manager import UserManager


credentials = Blueprint('credentials', __name__)


# noinspection PyUnresolvedReferences
@credentials.route('/credentials', methods=['POST', 'GET'])
@auto.doc(groups=['routes'])
@login_required
def _credentials():
    """
    Route from which users can modify their account data
    data which can be modified includes:
    - First name; Last name; email address; password
    The user will be prompted for confirmation before the changes are committed
    The user's old password is required to make edits

    :returns: a rendered view
    """
    form = CredentialsForm()
    kwargs = {}
    if request.method == 'POST':

        # check form validity
        if not form.validate_on_submit():
            return render_template('error_template.html', form=form)

        # check user authentication
        old_password = form.data['old_password']
        if not UserManager.authenticate(current_user.email, old_password):
            form.old_password.errors.append("Wrong Password!")
            return render_template('error_template.html', form=form)

        # display = ['email', 'firstname', 'lastname', 'password',
            # 'old_password']

        email = form.data["email"] if form.data["email"] != '' \
            else None
        firstname = form.data["firstname"] if form.data["firstname"] != '' \
            else None
        lastname = form.data["lastname"] if form.data["lastname"] != '' \
            else None
        password = form.data["password"] if form.data["password"] != '' \
            else None

        # check if the new mail already exists
        if email is not None and UserManager.exist_by_mail(email):
            form.email.errors.append("Email already in use")
            return render_template('error_template.html', form=form)

        # if no changes are submitted
        if not (email or firstname or lastname or password):
            form.email.errors.append("No changes specified")
            return render_template('error_template.html', form=form)

        # edit account data
        UserManager.edit_user(current_user.get_id(), email, firstname,
                              lastname, None, password)
        return redirect('/user_data')

    # no POST request
    else:
        return render_template('edit_credentials.html', form=form)
