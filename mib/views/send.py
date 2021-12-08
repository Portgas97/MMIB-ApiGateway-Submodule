import base64
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from mib.forms import SendForm
from mib.send import send_messages, save_draft
from mib.views.doc import auto
from mib.rao.message_manager import MessageManager as mm
from mib.views.utils import eprint

send = Blueprint('send', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """
    Checks the Allowed_Extensions constant to make sure we are sending an image

    :param filename: the file's name, extension included
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@send.route('/send', methods=['POST', 'GET'], defaults={'_id': None})
@send.route('/send/<_id>', methods=['POST', 'GET'])
@auto.doc(groups=['routes'])
@login_required
def _send(_id, data=""):
    """
    Endpoint for saving drafts and sending messages
    Takes values from the related form and either saves them as draft
    or passes the values on to the controller which will then proceed to queue
    the message with celery

    :param _id: the draft id
    :param data: a default parameter used for recipient setting
    :returns: a rendered view
    """
    form = SendForm()
    # if we are loading a draft:
    # the method check is required to avoid resetting the data on a POST
    if _id is not None and request.method == 'GET':
        # load it after checking its existence, and its status as a draft
        draft = None
        drafts = mm.get_box(current_user.email, 'drafts')
        for element in drafts:
            if element['id'] == int(_id):
                draft = element
                break
        if draft is None:
            abort(404)
        form.message.data = draft['message']
        form.recipient.data = draft['receiver_mail']
        form.time.data = \
            datetime.strptime(draft['time'], '%Y-%m-%d %H:%M:%S')
        form.image = draft['image']
        tmp_filename = draft['image']
        tmp_image = draft['image_hash']
    # instantiate arrays of mail addresses to display for our sender
    correctly_sent = []
    not_correctly_sent = []
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user_mail = current_user.email
            file = None
            # grab must-have data which we are guaranteed to have
            message, user_input = form.data['message'], form.data['recipient']
            time = form.data['time']
            to_parse = user_input.split(', ')
            # check if the post request has the optional file part
            tmp_image = ''
            tmp_filename = ''
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and allowed_file(file.filename):
                    tmp_image = base64.b64encode(file.read())
                    tmp_filename = secure_filename(file.filename)
                    if len(tmp_image) > 2000000:
                        form.file.errors.append(
                            "File too big, max of 2 MB")
                        return render_template(
                            'error_template.html',
                            form=form
                        )
            # we are saving a draft
            if request.form.get("save_button"):
                # save draft
                # unlike normal messages, drafts have multiple receivers
                # because they haven't been split yet
                if save_draft(_id, current_user_mail, user_input,
                              message, time, tmp_filename, tmp_image):
                    return redirect('/')
                else:
                    form.message.errors.append("Couldn't save the draft!")
                    return render_template(
                        'error_template.html',
                        form=form
                    )
            # we are sending a real message
            else:
                correctly_sent, not_correctly_sent = send_messages(
                    to_parse,
                    current_user_mail,
                    time,
                    message,
                    tmp_filename,
                    tmp_image
                )
        else:
            # noinspection PyUnresolvedReferences
            return render_template('error_template.html', form=form)
        # noinspection PyUnresolvedReferences
        return render_template(
            'done_sending.html',
            users1=correctly_sent,
            users2=not_correctly_sent,
            text=message
        )
    else:
        # noinspection PyUnresolvedReferences
        return render_template('send.html', form=form, use='send')


@send.route('/send_draft_list', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
def get_message():
    """
    View of all drafts for a given user

    :returns: a rendered view
    """
    drafts = mm.get_box(current_user.email, 'drafts')
    # noinspection PyUnresolvedReferences
    return render_template('list/draft_list.html', drafts=drafts, use='send')
