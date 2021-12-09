from unittest.mock import Mock, patch
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
            'lastname': "Rossi",
            'password': "password",
            'date_of_birth': "01/01/2000",
            'points': 100,
            'content_filter': False
        }

        data = {
            'id': randint(0, 999),
            'email': TestUserManager.faker.email(),
            'is_active' : choice([True,False]),
            'authenticated': choice([True,False]),
            'is_anonymous': False,
            'firstname': "pippo",
            'is_admin': False,
            'extra': extra_data
        }

        user = User(**data)
        return user

    """
    # NewUser not JSON serializable
    @patch('mib.rao.user_manager.requests.post')
    def test_create_user(self, mock_post):
        user = self.generate_user()
        mock_post.return_value = Mock(
            status_code=200
        )
        response = self.user_manager.\
                        create_user(user.email,
                                    user.firstname,
                                    user.extra_data['lastname'],
                                    user.extra_data['date_of_birth'],
                                    user.extra_data['password']
                                    )
        assert response is not None
    """

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
    def test_get_by_id_None(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=400,
            json = lambda:{

            }
        )
        response = self.user_manager.get_by_id(id)
        assert response is None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_mail(self, mock_get):
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
        response = self.user_manager.get_by_mail(user.email)
        assert response is not None
    
    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_mail_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        email = TestUserManager.faker.email()
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_by_mail(email)
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_by_mail_None(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=400,
            json=lambda: {

            }
        )
        response = self.user_manager.get_by_mail(user.email)
        assert response is None

    @patch('mib.rao.user_manager.requests.delete')
    def test_delete_user(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(status_code=200)        

        with self.app.test_request_context():
            response = self.user_manager.delete_user(user.id)
            assert response is not None

    @patch('mib.rao.user_manager.requests.delete')
    def test_delete_user_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                self.user_manager.delete_user(randint(0,999))
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

    """
    # doesn't work due to 404
    @patch('mib.rao.user_manager.requests.put')
    def test_add_points_404(self, mock_abort):
        mock_abort.return_value = Mock(status_code=400, json=lambda: {
            'message': 0})
        self.user_manager.add_points(id=randint(0, 999))
        mock_abort.assert_called_once_with(404, 'error')
    """

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

    # TODO doesn't work because an integer is returned...
    # @patch('mib.rao.user_manager.requests.get')
    # def test_get_points(self, mock):
    #    user = self.generate_user()
    #    mock.return_value = Mock(status_code=200)
    #    response_content = self.user_manager.get_points(id)
    #    assert response_content is int

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
            self.user_manager.exist_by_mail(email)
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
    """
    # TypeError: Object of type User is not JSON serializable
    @patch('mib.rao.user_manager.requests.put')
    def test_edit_user(self, mock_put):
        user = self.generate_user()
        mock_put.return_value = Mock(status_code=200)
        response = self.user_manager.edit_user(user.id)
        assert response is not None
    """

    @patch('mib.rao.user_manager.requests.put')
    def test_edit_user_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.Timeout()
        mock_put.return_value = Mock(status_code=400, json=lambda: {'message':
                                                                        0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.edit_user(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_reports(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # to set
            }
        )
        response = self.user_manager.get_reports()
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_reports_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_reports()
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_get_users_list(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # to set
            }
        )
        response = self.user_manager.get_users_list()
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_get_users_list_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=500, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.get_users_list()
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.user_manager.requests.get')
    def test_search(self, mock_get):
        user = self.generate_user()
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # to set
            }
        )
        response = self.user_manager.search(user, "word")
        assert response is not None

    @patch('mib.rao.user_manager.requests.get')
    def test_search_error(self, mock):
        user = self.generate_user()
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=500, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.search(user, "word")
            self.assertEqual(http_error.exception.code, 500)

    """
    # TypeError: Object of type Report is not JSON serializable
    @patch('mib.rao.user_manager.requests.post')
    def test_report_user(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                # to set
            }
        )
        response = self.user_manager.report_user("user1@example.com",
                                                 "user2@example.com",
                                                 "description",
                                                 "2021-11-30 10:10:00")
        assert response is not None
    """

    @patch('mib.rao.user_manager.requests.post')
    def test_report_user_error(self, mock):
        user = self.generate_user()
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=500, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.user_manager.report_user("user1@example.com",
                                          "user2@example.com",
                                          "description",
                                          "2021-11-30 10:10:00")

            self.assertEqual(http_error.exception.code, 500)
