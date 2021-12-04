import flask_login
from flask import Blueprint, render_template, request, abort
from flask_login.utils import login_required
from werkzeug.utils import redirect

from mib.forms import UnregisterForm
from mib.rao.user_manager import UserManager
from mib.views.doc import auto

unreg = Blueprint('unreg', __name__)


# noinspection PyUnresolvedReferences
@unreg.route('/unregister', methods=['GET', 'POST'])
@auto.doc(groups=['routes'])
@login_required
def unregister():
    """
    Deletes the caller's user account

    :return: a rendered view
    :raises: :class:`RuntimeError`:impossible conditions
    """
    form = UnregisterForm()

    if request.method == 'GET':
        return render_template("unregister.html", form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            password = form.data['password']
            _id = flask_login.current_user.id    # get user unique id
            email = flask_login.current_user.email

            # if the input password is correct, delete user account
            if UserManager.authenticate(email, password):
                UserManager.delete_user(_id)
                return redirect('/')
            # if the input password password is wrong, return a 401 status code
            else:
                abort(401)
    else:
        raise RuntimeError('This should not happen!')
