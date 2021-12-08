from flask import Blueprint, render_template, request
import flask_login
from flask_login.utils import login_required
from werkzeug.utils import redirect

from mib.auth.login_manager import admin_required
from mib.rao.user_manager import UserManager
from mib.forms import ReportForm
from datetime import datetime
from mib.rao.message_manager import MessageManager as mm
from mib.views.doc import auto

report = Blueprint('report', __name__)


@report.route('/reports', methods=['GET'])
@auto.doc(groups=['routes'])
@login_required
@admin_required
def reports():
    """
    The report management page for administrators

    :return: a rendered view
    """
    query_reports = UserManager.get_reports()
    return render_template("reports.html", reports=query_reports)


@report.route('/report_user', methods=['GET', 'POST'])
@auto.doc(groups=['routes'])
@login_required
def report_user():
    """
    Report a user to the admins

    :return: a rendered view
    """
    form = ReportForm()

    if request.method == 'GET':
        return render_template("report_user.html", form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            reported_user = form.data['user']
            description = form.data['description']
            block_user = form.data['block_user']
            current_user = flask_login.current_user
            current_user_email = current_user.email

            # a user cannot report himself
            if reported_user == current_user_email:
                form.user.errors.append("Cannot report yourself")
                return render_template('error_template.html', form=form)

            # create the report
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not UserManager.report_user(current_user_email, reported_user,
                                           description, timestamp):
                form.user.errors.append("Invalid mail error")
                return render_template('error_template.html', form=form)

            # blacklist reported user
            if block_user == 'yes':
                mm.add_blacklist(current_user_email, reported_user)

            return redirect('/')

    else:
        raise RuntimeError('This should not happen!')
