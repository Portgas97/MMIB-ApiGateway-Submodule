from flask import json
from werkzeug.security import check_password_hash
from mib import app
from flask import abort
import requests

from mib.auth.userauth import UserAuth
from mib.models.new_user import NewUser
from mib.models.user import User
from mib.models.report import Report
import sys


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def add_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code != 200:
            return abort(404)

    @classmethod
    def create_user(cls, email, firstname, lastname, date_of_birth, password):
        user = NewUser(email, firstname, lastname, password, date_of_birth)
        user = json.dumps(user)
        user = json.loads(user)
        print(user, file=sys.stderr)
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     json=user)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def decr_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.delete(url,
                                       timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code == 404:
            return abort(404)
        return response.status_code == 200

    @classmethod
    def delete_user(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.delete(url,
                                       timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)

    @classmethod
    def edit_user(cls, id, email=None, firstname=None,
                  lastname=None, date_of_birth=None, password=None):
        user = User(id, email, firstname, lastname, password, date_of_birth)
        # user.id = id
        # if email is not None:
        #     user.email = email
        # if firstname is not None:
        #     user.firstname = firstname
        # if lastname is not None:
        #     user.lastname = lastname
        # if password is not None:
        #     user.password = password
        # if date_of_birth is not None:
        #     user.date_of_birth = date_of_birth
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            user = json.dumps(user)
            user = json.loads(user)
            response = requests.put(url,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                    json=user)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def exist_by_id(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.head(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def exist_by_mail(cls, email):
        try:
            url = ("%s/users/by_mail/" % cls.USERS_ENDPOINT) + email
            response = requests.head(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def get_by_id(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def get_by_mail(cls, email):
        try:
            url = ("%s/users/by_mail/" % cls.USERS_ENDPOINT) + email
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def get_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code == 200:
            return int(response.content)
        else:
            return abort(404)

    @classmethod
    def get_reports(cls):
        try:
            url = "%s/report" % cls.USERS_ENDPOINT
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.content

    @classmethod
    def get_users_list(cls):
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.json()

    @classmethod
    def report_user(cls, author, reported, description, timestamp):
        report = Report(None, author, reported, description, timestamp)
        # report.author_email = author
        # report.reported_email = reported
        # report.description = description
        # report.timestamp = timestamp
        try:
            url = "%s/report" % cls.USERS_ENDPOINT
            report = json.dumps(report)
            report = json.loads(report)
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     json=report)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def set_filter(cls, id):
        try:
            url = "%s/filter/%s" % (cls.USERS_ENDPOINT, str(id))
            requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)

    @classmethod
    def unset_filter(cls, id):
        try:
            url = "%s/filter/%s" % (cls.USERS_ENDPOINT, str(id))
            requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.get_by_mail(email)
        if user is None:
            return False
        hash = user['password']
        if not check_password_hash(hash, password):
            return None
        return UserAuth(id=user['id'], email=user['email'])
