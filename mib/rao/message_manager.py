from flask import json
from mib import app
from flask import abort
import requests

from mib.models.draft import Draft
from mib.models.message import Message

from mib import encoder


class MessageManager:
    MESSAGES_ENDPOINT = app.config['MESSAGES_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']

    @classmethod
    def get_blacklist(cls, owner):
        try:
            url = "%s/blacklist/%s" % (cls.MESSAGES_ENDPOINT, owner)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code != 200:
            return []
        else:
            return response.json()

    @classmethod
    def check_blacklist(cls, owner, email):
        try:
            url = "%s/blacklist" % cls.MESSAGES_ENDPOINT
            query_string = {'owner': owner, 'email': email}
            response = requests.head(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                params=query_string
            )
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def add_blacklist(cls, owner, email):
        try:
            url = "%s/blacklist" % cls.MESSAGES_ENDPOINT
            query_string = {'owner': owner, 'email': email}
            response = requests.put(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                params=query_string
            )
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def remove_blacklist(cls, owner, email):
        try:
            url = "%s/blacklist" % cls.MESSAGES_ENDPOINT
            query_string = {'owner': owner, 'email': email}
            response = requests.delete(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                params=query_string
            )
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def create_draft(cls, message, sender, receiver, time, image, image_hash):
        draft = Message(None, sender, receiver,
                        message, time, image, image_hash)
        try:
            url = "%s/draft" % cls.MESSAGES_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dumps(draft),
                                     headers=encoder.headers)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def delete_draft(cls, id: int):
        try:
            url = "%s/draft/%s" % (cls.MESSAGES_ENDPOINT, str(id))
            response = requests.delete(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS
            )
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def create_message(
            cls, message, sender, receiver, time, image, image_hash):
        message = Message(
            None,
            sender,
            receiver,
            message,
            time,
            image,
            image_hash
        )
        try:
            url = "%s/message" % cls.MESSAGES_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dumps(message),
                                     headers=encoder.headers)
            return response.json()
        except Exception:
            abort(500)

    @classmethod
    def delete_message(cls, owner: str, id: int):
        query_string = {'email': owner, 'id': id}
        try:
            url = "%s/message" % cls.MESSAGES_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     params=query_string)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def withdraw(cls, id: int):
        try:
            url = "%s/withdraw/%s" % (cls.MESSAGES_ENDPOINT, str(id))
            response = requests.delete(
                url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def edit_draft(cls, id, message, sender, receiver, time, image, img_hash):
        draft = Draft(id, sender, receiver, message, time, image, img_hash)
        try:
            url = "%s/draft" % cls.MESSAGES_ENDPOINT
            response = requests.put(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                data=json.dumps(draft),
                headers=encoder.headers)
        except Exception:
            return abort(500)
        return response.status_code == 200

    @classmethod
    def get_box(cls, owner: str, box: str):
        """get the inbox/draft/outbox

        Obtains a json containing all values for that box for the specified
        user, 404 if none are present

        :param owner: email address
        :param box: [inbox, drafts, outbox]
        """
        try:
            url = "%s/%s/%s" % (cls.MESSAGES_ENDPOINT, box, owner)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        else:
            return abort(404)

    @classmethod
    def set_as_read(cls, id: int):
        try:
            url = "%s/message/%s" % (cls.MESSAGES_ENDPOINT, str(id))
            response = requests.put(
                url,
                timeout=cls.REQUESTS_TIMEOUT_SECONDS
            )
        except Exception:
            return abort(500)
        return response.status_code == 200
