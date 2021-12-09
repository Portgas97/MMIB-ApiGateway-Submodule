from unittest.mock import Mock, patch
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests
import sys  # for debugging
import json
from mib.models.notification import Notification
from .rao_test import RaoTest


class TestNotificationManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestNotificationManager, self).setUp()
        from mib.rao.notifications_manager import NotificationsManager
        self.notifications_manager = NotificationsManager
        from mib import app
        self.app = app

    def generate_notification(self):
        notification = Notification()
        notification.user_email = TestNotificationManager.faker.email(),
        notification.title = "fake_title"
        notification.description = "fake_description"
        notification.timestamp = "2021-11-30 10:10:00"
        notification.message_id = randint(0, 999)
        return notification

    # TODO: problem, it says that Notification object is not JSON serializable
    """
    @patch('mib.rao.notifications_manager.requests.post')
    def test_create_notification(self, mock_post):
        notification = self.generate_notification()

        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                'id': notification.id
            }
        )
        response = self.notifications_manager.create_notification(
            notification.user_email,
            notification.title,
            notification.description,
            notification.timestamp,
            notification.message_id
        )
        assert response is not None
    """

    @patch('mib.rao.notifications_manager.requests.post')
    def test_create_notification_error(self, mock_post):
        notification = self.generate_notification()
        mock_post.side_effect = requests.exceptions.Timeout()
        mock_post.return_value = Mock(status_code=400,
                                      json=lambda: {'message': 0})
        with self.app.test_request_context():
            with self.assertRaises(HTTPException) as http_error:
                self.notifications_manager.create_notification(
                    self.faker.email(),
                    notification.title,
                    notification.description,
                    notification.timestamp,
                    notification.message_id
                )
                self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.notifications_manager.requests.delete')
    def test_delete_notification(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)
        response = self.notifications_manager.delete_notification("1")
        import sys
        sys.stderr.write(str(response))
        assert response is not None

    @patch('mib.rao.notifications_manager.requests.delete')
    def test_set_filter_error(self, mock_delete):
        mock_delete.side_effect = requests.exceptions.Timeout()
        mock_delete.return_value = Mock(status_code=400, json=lambda: {
            'message':
                                                                        0})
        with self.assertRaises(HTTPException) as http_error:
            self.notifications_manager.delete_notification(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.notifications_manager.requests.get')
    def test_get_notifications(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # I don't know what to put there
            }
        )
        response = self.notifications_manager.get_notifications("user")
        # import sys
        # sys.stderr.write(str(response))
        assert response is not None

    @patch('mib.rao.notifications_manager.requests.get')
    def test_get_notifications_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(status_code=400, json=lambda: {
            'message':
                0})
        with self.assertRaises(HTTPException) as http_error:
            self.notifications_manager.get_notifications("user")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.notifications_manager.requests.get')
    def test_get_notifications_None(self, mock_get):
        mock_get.return_value = Mock(status_code=400)
        response = self.notifications_manager.get_notifications("user")
        assert response is None

    @patch('mib.rao.notifications_manager.requests.get')
    def test_notifications_count(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # I don't know what to put there
            }
        )
        response = self.notifications_manager.notifications_count("user")
        # import sys
        # sys.stderr.write(str(response))
        assert response is not None

    @patch('mib.rao.notifications_manager.requests.get')
    def test_notifications_count_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(status_code=400, json=lambda: {
            'message':
                0})
        with self.assertRaises(HTTPException) as http_error:
            self.notifications_manager.notifications_count("bad_user")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.notifications_manager.requests.get')
    def test_notifications_count_None(self, mock_get):
        mock_get.return_value = Mock(status_code=400)
        response = self.notifications_manager.notifications_count("user")
        assert response is None

    @patch('mib.rao.notifications_manager.requests.put')
    def test_set_notifications_as_read(self, mock_put):
        mock_put.return_value = Mock(status_code=200)
        response = self.notifications_manager.set_notifications_as_read("user")
        assert response is not None

    @patch('mib.rao.notifications_manager.requests.put')
    def test_set_notifications_as_read_error(self, mock_put):
        mock_put.side_effect = requests.exceptions.Timeout()
        mock_put.return_value = Mock(status_code=400, json=lambda: {
            'message':0})
        with self.assertRaises(HTTPException) as http_error:
            self.notifications_manager.set_notifications_as_read("bad_user")
            self.assertEqual(http_error.exception.code, 500)

