from flask import Blueprint, render_template, request, redirect, \
    url_for, jsonify
from flask_login import login_required
from werkzeug.exceptions import BadRequestKeyError

from flask_login import current_user
from mib.forms import RecipientsListForm
from mib.rao.user_manager import UserManager
from mib.views.doc import auto

list_blueprint = Blueprint('list', __name__)


# noinspection PyUnresolvedReferences
@list_blueprint.route('/list_of_recipients', methods=['POST', 'GET'])
@auto.doc(groups=['routes'])
@login_required
def _display_users():
    """
    Displays a page with a searchable list of registered users
    which can then be selected as recipients

    :returns: a rendered view
    """

    if request.method == 'POST':  # POST request
        if len(request.form) != 0:  # check the selection of a recipient
            # create a list of emails, removing the submitted label
            selected_recipient_list = \
                request.form.getlist('multiple_field_form')
            # create a dictionary to construct the right structure
            payload = {'email_list': ', '.join(selected_recipient_list)}
            # send a list of comma-separated emails
            # redirecting to /send
            return redirect(url_for('send._send', data=payload['email_list']))

        else:  # no recipient selected
            return redirect(url_for('send._send'))

    else:  # GET request, returns the list_of_recipients.html page
        return render_template('list_of_recipients.html')


# noinspection PyUnresolvedReferences
@list_blueprint.route('/live_search', methods=['POST'])
@auto.doc(groups=['routes'])
@login_required
def ajax_livesearch():
    """
    The live search function for the user list

    :return: a list of addresses matching the search query, excluding the
    caller's address
    :rtype: json string
    """
    user_list = UserManager.get_users_list()
    # to filter the current_user from the list
    user_list = filter(lambda user: user["id"] != current_user.id, user_list)
    try:
        search_word = request.form['query']
    except BadRequestKeyError:
        recipients_found = user_list
    else:
        if request.form['query'] == 'void_request':
            recipients_found = user_list
        else:
            def filter_users(user):
                return search_word in user["email"] or search_word in user[
                    "firstname"] or search_word in user["lastname"]
            recipients_found = filter(filter_users, user_list)

    # instantiate the form
    form = RecipientsListForm()

    # sets choices
    form.multiple_field_form.choices = \
        [(user['email'], user['lastname'] + ' ' + user['firstname'] + ': ' + user['email'])
         for user in recipients_found]

    return jsonify(
        {'htmlresponse': render_template('search_response.html', form=form)})
