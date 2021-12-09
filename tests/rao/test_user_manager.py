from unittest.mock import Mock, patch
from flask import current_app
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests

from mib.auth.userauth import UserAuth as User
from .rao_test import RaoTest


class TestUserManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestUserManager, self).setUp()
        from mib.rao.user_manager import UserManager
        self.user_manager = UserManager
        from mib import app
        self.app = app

    def generate_user(self):
        extra_data = {
            'firstname': "Mario",
            'lastname': "Rossi",
            'password': "password",
            'date_of_birth': "01/01/2000",
            'points': 100,
            'content_filter': False,
            'is_admin': False
        }

        data = {
            'id': randint(0, 999),
            'email': TestUserManager.faker.email(),
            'is_active' : choice([True,False]),
            'authenticated': choice([True,False]),
            'is_anonymous': False,
            'extra': extra_data
        }

        user = User(**data)
        return user

    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_id(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json = lambda:{
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False
            }
        )
        response = self.user_manager.get_by_id(id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_id_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_email(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                'id':user.id,
                'email':user.email,
                'is_active': False,
                'authenticated': False,
                'is_anonymous': False
            }
        )
        response = self.user_manager.get_by_email(user.email)
        assert response is not None
    
    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_email_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        email = TestUserManager.faker.email()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_by_email(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.delete')
    def test_delete_user(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(status_code=200)        

        with self.app.test_request_context():
            response = self.user_manager.delete_user(user_id=user.id)            
            assert response is not None

    @patch('mib.rao.user_manager.requests.delete')
    def test_delete_user_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                self.user_manager.delete_user(user_id=randint(0,999))
                self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.put')
    def test_add_points(self, mock_put):
        user = self.generate_user()
        mock_put.return_value = Mock(status_code=200)
        response = self.user_manager.add_points(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.put')
    def test_add_points_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.Timeout()
        mock_put.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                      0})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                self.user_manager.add_points(id=randint(0, 999))
                self.assertEqual(http_error.exception.code, 500)

    # doesn't return a well-formed response
    @patch('mib.rao.user_manager.requests.delete')
    def test_decr_points(self, mock_delete):
        pass

    # TODO
    @patch('mib.rao.user_manager.requests.delete')
    def test_decr_points_error(self, mock_delete):
        pass

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_id(self, mock_head):
        user = self.generate_user()
        mock_head.return_value = Mock(status_code=200)
        response = self.user_manager.exist_by_id(id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_id_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.Timeout()
        mock_head.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                     0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.exist_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_points(self, mock):
        user = self.generate_user()
        mock.return_value = Mock(status_code=200)
        response_content = self.user_manager.get_points(id)
        assert response_content is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_points_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                         0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_points(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_id(self, mock_head):
        user = self.generate_user()
        mock_head.return_value = Mock(status_code=200)
        response = self.user_manager.exist_by_id(id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_id_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.Timeout()
        mock_head.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                    0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.exist_by_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_mail(self, mock_head):
        user = self.generate_user()
        mock_head.return_value = Mock(status_code=200)
        response = self.user_manager.exist_by_mail(user.email)
        assert response is not None

    @patch('mib.rao.user_manager.requests.head')
    def test_exist_by_mail_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.Timeout()
        mock_head.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                         0})
        email = TestUserManager.faker.email()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.exist_by_id(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.put')
    def test_set_filter(self, mock_put):
        user = self.generate_user()
        mock_put.return_value = Mock(status_code=200)
        response = self.user_manager.set_filter(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.put')
    def test_set_filter_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.Timeout()
        mock_put.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                         0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.set_filter(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.delete')
    def test_unset_filter(self, mock_delete):
        user = self.generate_user()
        mock_delete.return_value = Mock(status_code=200)
        response = self.user_manager.unset_filter(user.id)
        assert response is not None

    @patch('mib.rao.user_manager.requests.delete')
    def test_set_filter_error(self, mock_delete):
        mock_delete.side_effect = requests.exceptions.Timeout()
        mock_delete.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                        0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.unset_filter(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    # TODO: get_reports, get_users_list, search, report_user

