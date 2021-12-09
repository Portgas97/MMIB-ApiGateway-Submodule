import requests
from flask import abort
from flask import json
from werkzeug.security import check_password_hash

from mib import app
from mib import encoder
from mib.auth.userauth import UserAuth
from mib.models.new_user import NewUser
from mib.models.report import Report
from mib.models.user import User


class UserManager:
    """
    This class is an interface with the User-Service microservice.
    See the User-Service's documentation for more details on the methods.
    """
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
        return response

    @classmethod
    def create_user(cls, email, firstname, lastname, date_of_birth, password):
        user = NewUser(email, firstname, lastname, password, date_of_birth)
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dumps(user),
                                     headers=encoder.headers)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def decr_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.delete(url,
                                       timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code == 404:
            return abort(404)
        return response.status_code == 200

    @classmethod
    def delete_user(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)

    @classmethod
    def edit_user(cls, id, email=None, firstname=None,
                  lastname=None, date_of_birth=None, password=None):
        user = User(id, email, firstname, lastname, password, date_of_birth)
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.put(url,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                    data=json.dumps(user),
                                    headers=encoder.headers)
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
        except Exception:
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
        return response.json()

    @classmethod
    def get_users_list(cls):
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.json()

    @classmethod
    def search(cls, caller, word=None):
        if word is None:
            params = [('caller', caller)]
        else:
            params = [('caller', caller), ('word', word)]
        try:
            url = "%s/search" % cls.USERS_ENDPOINT
            response = requests.get(url,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                    params=params)
        except Exception:
            return abort(500)
        return response.json()

    @classmethod
    def report_user(cls, author, reported, description, timestamp):
        report = Report(None, author, reported, description, timestamp)
        try:
            url = "%s/report" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dumps(report),
                                     headers=encoder.headers)
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
        """
        Authenticate a user by email and password,
        return the corresponding UserAuth object.
        :param email: the email of the user
        :param password: the password of the user
        :return: the UserAuth object corresponding to the email owner
        """
        user = cls.get_by_mail(email)
        if user is None:
            return None
        hash = user['password']
        if not check_password_hash(hash, password):
            return None
        return UserAuth(**user)
