# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mib.models.base_model_ import Model
from mib.models import util


class Notification(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: int=None, user_email: str=None, title: str=None, description: str=None, timestamp: str=None, status: int=None, message_id: int=None, is_read: bool=None, is_deleted: bool=None):  # noqa: E501
        """Notification - a model defined in Swagger

        :param id: The id of this Notification.  # noqa: E501
        :type id: int
        :param user_email: The user_email of this Notification.  # noqa: E501
        :type user_email: str
        :param title: The title of this Notification.  # noqa: E501
        :type title: str
        :param description: The description of this Notification.  # noqa: E501
        :type description: str
        :param timestamp: The timestamp of this Notification.  # noqa: E501
        :type timestamp: str
        :param status: The status of this Notification.  # noqa: E501
        :type status: int
        :param message_id: The message_id of this Notification.  # noqa: E501
        :type message_id: int
        :param is_read: The is_read of this Notification.  # noqa: E501
        :type is_read: bool
        :param is_deleted: The is_deleted of this Notification.  # noqa: E501
        :type is_deleted: bool
        """
        self.swagger_types = {
            'id': int,
            'user_email': str,
            'title': str,
            'description': str,
            'timestamp': str,
            'status': int,
            'message_id': int,
            'is_read': bool,
            'is_deleted': bool
        }

        self.attribute_map = {
            'id': 'id',
            'user_email': 'user_email',
            'title': 'title',
            'description': 'description',
            'timestamp': 'timestamp',
            'status': 'status',
            'message_id': 'message_id',
            'is_read': 'is_read',
            'is_deleted': 'is_deleted'
        }

        self._id = id
        self._user_email = user_email
        self._title = title
        self._description = description
        self._timestamp = timestamp
        self._status = status
        self._message_id = message_id
        self._is_read = is_read
        self._is_deleted = is_deleted

    @classmethod
    def from_dict(cls, dikt) -> 'Notification':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Notification of this Notification.  # noqa: E501
        :rtype: Notification
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Notification.


        :return: The id of this Notification.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Notification.


        :param id: The id of this Notification.
        :type id: int
        """

        self._id = id

    @property
    def user_email(self) -> str:
        """Gets the user_email of this Notification.


        :return: The user_email of this Notification.
        :rtype: str
        """
        return self._user_email

    @user_email.setter
    def user_email(self, user_email: str):
        """Sets the user_email of this Notification.


        :param user_email: The user_email of this Notification.
        :type user_email: str
        """
        if user_email is None:
            raise ValueError("Invalid value for `user_email`, must not be `None`")  # noqa: E501

        self._user_email = user_email

    @property
    def title(self) -> str:
        """Gets the title of this Notification.


        :return: The title of this Notification.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Notification.


        :param title: The title of this Notification.
        :type title: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def description(self) -> str:
        """Gets the description of this Notification.


        :return: The description of this Notification.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Notification.


        :param description: The description of this Notification.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def timestamp(self) -> str:
        """Gets the timestamp of this Notification.


        :return: The timestamp of this Notification.
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str):
        """Sets the timestamp of this Notification.


        :param timestamp: The timestamp of this Notification.
        :type timestamp: str
        """
        if timestamp is None:
            raise ValueError("Invalid value for `timestamp`, must not be `None`")  # noqa: E501

        self._timestamp = timestamp

    @property
    def status(self) -> int:
        """Gets the status of this Notification.


        :return: The status of this Notification.
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status: int):
        """Sets the status of this Notification.


        :param status: The status of this Notification.
        :type status: int
        """

        self._status = status

    @property
    def message_id(self) -> int:
        """Gets the message_id of this Notification.


        :return: The message_id of this Notification.
        :rtype: int
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id: int):
        """Sets the message_id of this Notification.


        :param message_id: The message_id of this Notification.
        :type message_id: int
        """

        self._message_id = message_id

    @property
    def is_read(self) -> bool:
        """Gets the is_read of this Notification.


        :return: The is_read of this Notification.
        :rtype: bool
        """
        return self._is_read

    @is_read.setter
    def is_read(self, is_read: bool):
        """Sets the is_read of this Notification.


        :param is_read: The is_read of this Notification.
        :type is_read: bool
        """

        self._is_read = is_read

    @property
    def is_deleted(self) -> bool:
        """Gets the is_deleted of this Notification.


        :return: The is_deleted of this Notification.
        :rtype: bool
        """
        return self._is_deleted

    @is_deleted.setter
    def is_deleted(self, is_deleted: bool):
        """Sets the is_deleted of this Notification.


        :param is_deleted: The is_deleted of this Notification.
        :type is_deleted: bool
        """

        self._is_deleted = is_deleted
