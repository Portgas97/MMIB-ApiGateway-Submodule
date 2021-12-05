from flask import json
from werkzeug.security import check_password_hash
from mib import app
from flask import abort
import requests

from mib.models.notification import Notification
import sys
from mib import encoder


class NotificationsManager:
    NOTIFICATIONS_ENDPOINT = app.config['NOTIFICATIONS_MS_URL']
    REQUESTS_TIMEOUT_SECONDS = app.config['REQUESTS_TIMEOUT_SECONDS']


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
