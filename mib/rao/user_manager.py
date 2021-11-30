import json

from werkzeug.security import check_password_hash

from mib import app
from flask_login import (logout_user)
from flask import abort
import requests

from mib.swagger_client.models import User, NewUser, Report


class UserManager:
    USERS_ENDPOINT = app.config['USERS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def add_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code != 200:
            return abort(404)

    @classmethod
    def create_user(cls, email, firstname, lastname, date_of_birth, password):
        user = NewUser()
        user.email = email
        user.firstname = firstname
        user.lastname = lastname
        user.password = password
        user.date_of_birth = date_of_birth
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dump(user))
        except:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def decr_points(cls, id):
        try:
            url = "%s/points/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code == 404:
            return abort(404)
        return response.status_code == 200


    @classmethod
    def delete_user(cls, id):
        try:
            url = "%s/users/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)


    @classmethod
    def edit_user(cls, id, email=None, firstname=None,
                  lastname=None, date_of_birth=None, password=None):
        user = User()
        if email is not None:
            user.email = email
        if firstname is not None:
            user.firstname = firstname
        if lastname is not None:
            user.lastname = lastname
        if password is not None:
            user.password = password
        if date_of_birth is not None:
            user.date_of_birth = date_of_birth
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.put(url,
                                    timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                    data=json.dump(user))
        except:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def exist_by_id(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.head(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def exist_by_mail(cls, email):
        try:
            url = ("%s/users/by_mail/" % cls.USERS_ENDPOINT) + email
            response = requests.head(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def get_by_id(cls, id):
        try:
            url = "%s/users/by_id/%s" % (cls.USERS_ENDPOINT, str(id))
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def get_by_mail(cls, email):
        try:
            url = ("%s/users/by_mail/" % cls.USERS_ENDPOINT) + email
            response = requests.head(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
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
        except:
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
        except:
            return abort(500)
        return response.json()

    @classmethod
    def get_users_list(cls):
        try:
            url = "%s/users" % cls.USERS_ENDPOINT
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        return response.json()

    @classmethod
    def report_user(cls, author, reported, description, timestamp):
        report = Report()
        report.author_email = author
        report.reported_email = reported
        report.description = description
        report.timestamp = timestamp
        try:
            url = "%s/report" % cls.USERS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dump(report))
        except:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def set_filter(cls, id):
        try:
            url = "%s/filter/%s" % (cls.USERS_ENDPOINT, str(id))
            requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)

    @classmethod
    def unset_filter(cls, id):
        try:
            url = "%s/filter/%s" % (cls.USERS_ENDPOINT, str(id))
            requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.get_by_mail(email)
        if user is None:
            return False
        hash = user['password']
        return check_password_hash(hash, password)

    # @classmethod
    # def get_user_by_id(cls, user_id: int) -> User:
    #     """
    #     This method contacts the users microservice
    #     and retrieves the user object by user id.
    #     :param user_id: the user id
    #     :return: User obj with id=user_id
    #     """
    #     try:
    #         response = requests.get("%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id)),
    #                                 timeout=cls.REQUESTS_TIMEOUT_SECONDS)
    #         json_payload = response.json()
    #         if response.status_code == 200:
    #             # user is authenticated
    #             user = User.build_from_json(json_payload)
    #         else:
    #             raise RuntimeError('Server has sent an unrecognized status code %s' % response.status_code)
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     return user
    #
    # @classmethod
    # def get_user_by_email(cls, user_email: str):
    #     """
    #     This method contacts the users microservice
    #     and retrieves the user object by user email.
    #     :param user_email: the user email
    #     :return: User obj with email=user_email
    #     """
    #     try:
    #         response = requests.get("%s/user_email/%s" % (cls.USERS_ENDPOINT, user_email),
    #                                 timeout=cls.REQUESTS_TIMEOUT_SECONDS)
    #         json_payload = response.json()
    #         user = None
    #
    #         if response.status_code == 200:
    #             user = User.build_from_json(json_payload)
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     return user
    #
    # @classmethod
    # def get_user_by_phone(cls, user_phone: str) -> User:
    #     """
    #     This method contacts the users microservice
    #     and retrieves the user object by user phone.
    #     :param user_phone: the user phone
    #     :return: User obj with phone=user_phone
    #     """
    #     try:
    #         response = requests.get("%s/user_phone/%s" % (cls.USERS_ENDPOINT, user_phone),
    #                                 timeout=cls.REQUESTS_TIMEOUT_SECONDS)
    #         json_payload = response.json()
    #         user = None
    #
    #         if response.status_code == 200:
    #             user = User.build_from_json(json_payload)
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     return user
    #
    # @classmethod
    # def create_user(cls,
    #                 email: str, password: str,
    #                 firstname: str, lastname: str,
    #                 birthdate, phone: str):
    #     try:
    #         url = "%s/user" % cls.USERS_ENDPOINT
    #         response = requests.post(url,
    #                                  json={
    #                                      'email': email,
    #                                      'password': password,
    #                                      'firstname': firstname,
    #                                      'lastname': lastname,
    #                                      'birthdate': birthdate,
    #                                      'phone': phone
    #                                  },
    #                                  timeout=cls.REQUESTS_TIMEOUT_SECONDS
    #                                  )
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     return response
    #
    # @classmethod
    # def update_user(cls, user_id: int, email: str, password: str, phone: str):
    #     """
    #     This method contacts the users microservice
    #     to allow the users to update their profiles
    #     :param phone:
    #     :param password:
    #     :param email:
    #     :param user_id: the customer id
    #         email: the user email
    #         password: the user password
    #         phone: the user phone
    #     :return: User updated
    #     """
    #     try:
    #         url = "%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id))
    #         response = requests.put(url,
    #                                 json={
    #                                     'email': email,
    #                                     'password': password,
    #                                     'phone': phone
    #                                 },
    #                                 timeout=cls.REQUESTS_TIMEOUT_SECONDS
    #                                 )
    #         return response
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     raise RuntimeError('Error with searching for the user %s' % user_id)
    #
    # @classmethod
    # def delete_user(cls, user_id: int):
    #     """
    #     This method contacts the users microservice
    #     to delete the account of the user
    #     :param user_id: the user id
    #     :return: User updated
    #     """
    #     try:
    #         logout_user()
    #         url = "%s/user/%s" % (cls.USERS_ENDPOINT, str(user_id))
    #         response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
    #
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         return abort(500)
    #
    #     return response
    #
    # @classmethod
    # def authenticate_user(cls, email: str, password: str) -> User:
    #     """
    #     This method authenticates the user trough users AP
    #     :param email: user email
    #     :param password: user password
    #     :return: None if credentials are not correct, User instance if credentials are correct.
    #     """
    #     payload = dict(email=email, password=password)
    #     try:
    #         print('trying response....')
    #         response = requests.post('%s/authenticate' % cls.USERS_ENDPOINT,
    #                                  json=payload,
    #                                  timeout=cls.REQUESTS_TIMEOUT_SECONDS
    #                                  )
    #         print('received response....')
    #         json_response = response.json()
    #     except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    #         # We can't connect to Users MS
    #         return abort(500)
    #
    #     if response.status_code == 401:
    #         # user is not authenticated
    #         return None
    #     elif response.status_code == 200:
    #         user = User.build_from_json(json_response['user'])
    #         return user
    #     else:
    #         raise RuntimeError(
    #             'Microservice users returned an invalid status code %s, and message %s'
    #             % (response.status_code, json_response['error_message'])
    #         )
