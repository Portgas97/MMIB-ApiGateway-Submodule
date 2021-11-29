# coding: utf-8

"""
    Users

    Microservice that provide users' data management.  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: you@your-company.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from monolith.swagger_client.configuration import Configuration


class NewUser(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'email': 'str',
        'firstname': 'str',
        'lastname': 'str',
        'password': 'str',
        'date_of_birth': 'str'
    }

    attribute_map = {
        'email': 'email',
        'firstname': 'firstname',
        'lastname': 'lastname',
        'password': 'password',
        'date_of_birth': 'date_of_birth'
    }

    def __init__(self, email=None, firstname=None, lastname=None, password=None, date_of_birth=None, _configuration=None):  # noqa: E501
        """NewUser - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._email = None
        self._firstname = None
        self._lastname = None
        self._password = None
        self._date_of_birth = None
        self.discriminator = None

        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.date_of_birth = date_of_birth

    @property
    def email(self):
        """Gets the email of this NewUser.  # noqa: E501


        :return: The email of this NewUser.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this NewUser.


        :param email: The email of this NewUser.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and email is None:
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def firstname(self):
        """Gets the firstname of this NewUser.  # noqa: E501


        :return: The firstname of this NewUser.  # noqa: E501
        :rtype: str
        """
        return self._firstname

    @firstname.setter
    def firstname(self, firstname):
        """Sets the firstname of this NewUser.


        :param firstname: The firstname of this NewUser.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and firstname is None:
            raise ValueError("Invalid value for `firstname`, must not be `None`")  # noqa: E501

        self._firstname = firstname

    @property
    def lastname(self):
        """Gets the lastname of this NewUser.  # noqa: E501


        :return: The lastname of this NewUser.  # noqa: E501
        :rtype: str
        """
        return self._lastname

    @lastname.setter
    def lastname(self, lastname):
        """Sets the lastname of this NewUser.


        :param lastname: The lastname of this NewUser.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and lastname is None:
            raise ValueError("Invalid value for `lastname`, must not be `None`")  # noqa: E501

        self._lastname = lastname

    @property
    def password(self):
        """Gets the password of this NewUser.  # noqa: E501


        :return: The password of this NewUser.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this NewUser.


        :param password: The password of this NewUser.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password

    @property
    def date_of_birth(self):
        """Gets the date_of_birth of this NewUser.  # noqa: E501


        :return: The date_of_birth of this NewUser.  # noqa: E501
        :rtype: str
        """
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        """Sets the date_of_birth of this NewUser.


        :param date_of_birth: The date_of_birth of this NewUser.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and date_of_birth is None:
            raise ValueError("Invalid value for `date_of_birth`, must not be `None`")  # noqa: E501

        self._date_of_birth = date_of_birth

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(NewUser, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NewUser):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewUser):
            return True

        return self.to_dict() != other.to_dict()
