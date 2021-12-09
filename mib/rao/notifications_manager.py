import requests
from flask import abort
from flask import json

from mib import app
from mib import encoder
from mib.models.notification import Notification


class NotificationsManager:
    NOTIFICATIONS_ENDPOINT = app.config['NOTIFICATIONS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']


    @classmethod
    def create_notification(cls, email, title, desctiption, timestamp, message_id):
        notification = Notification()
        notification.user_email = email
        notification.title = title
        notification.description = desctiption
        notification.timestamp = timestamp
        notification.message_id = message_id

        try:
            url = "%s/notification" % cls.NOTIFICATIONS_ENDPOINT
            response = requests.post(url,
                                     timeout=cls.REQUESTS_TIMEOUT_SECONDS,
                                     data=json.dumps(notification),
                                     headers=encoder.headers)
        except Exception:
            return abort(500)

        return response.json()



    @classmethod
    def delete_notification(cls, message):
        try:
            url = "%s/notification/%s" % (cls.NOTIFICATIONS_ENDPOINT, str(message))
            response = requests.delete(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.status_code


    @classmethod
    def get_notifications(cls, user):
        try:
            url = ("%s/notifications/" % cls.NOTIFICATIONS_ENDPOINT) + user
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        return None


    @classmethod
    def notifications_count(cls, user):
        try:
            url = "%s/notifications/count/%s" % (cls.NOTIFICATIONS_ENDPOINT, user)
            response = requests.get(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        if response.status_code == 200:
            return response.json()
        return None


    @classmethod
    def set_notifications_as_read(cls, user):
        try:
            url = "%s/notifications/%s" % (cls.NOTIFICATIONS_ENDPOINT, user)
            response = requests.put(url, timeout=cls.REQUESTS_TIMEOUT_SECONDS)
        except Exception:
            return abort(500)
        return response.status_code 
