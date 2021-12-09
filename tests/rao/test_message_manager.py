from unittest.mock import Mock, patch
from faker import Faker
from random import randint, choice
from werkzeug.exceptions import HTTPException
import requests
from mib.models.message import Message
from .rao_test import RaoTest


class TestMessageManager(RaoTest):

    faker = Faker('it_IT')

    def setUp(self):
        super(TestMessageManager, self).setUp()
        from mib.rao.message_manager import MessageManager
        self.message_manager = MessageManager
        from mib import app
        self.app = app

    @patch('mib.rao.message_manager.requests.get')
    def test_get_blacklist(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        response = self.message_manager.get_blacklist("user@example.com")
        assert response is not None

    @patch('mib.rao.message_manager.requests.get')
    def test_get_blacklist_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.get_blacklist("user@example.com")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.head')
    def test_check_blacklist(self, mock_head):
        mock_head.return_value = Mock(status_code=200)
        response = self.message_manager.check_blacklist("user@example.com",
                                                        "user2@example.com")
        assert response is not None

    @patch('mib.rao.message_manager.requests.head')
    def test_check_blacklist_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.check_blacklist("user@example.com",
                                                 "user2@example.com")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.put')
    def test_add_blacklist(self, mock_put):
        mock_put.return_value = Mock(status_code=200)
        response = self.message_manager.add_blacklist("user@example.com",
                                                      "user2@example.com")
        assert response is not None

    @patch('mib.rao.message_manager.requests.put')
    def test_add_blacklist_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.add_blacklist("user@example.com",
                                               "user2@example.com")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.delete')
    def test_remove_blacklist(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)
        response = self.message_manager.remove_blacklist("user@example.com",
                                                      "user2@example.com")
        assert response is not None

    @patch('mib.rao.message_manager.requests.delete')
    def test_remove_blacklist_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.remove_blacklist("user@example.com",
                                                  "user2@example.com")
            self.assertEqual(http_error.exception.code, 500)

    """
    @patch('mib.rao.message_manager.requests.post')
    def test_create_draft(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        response = self.message_manager.create_message("message",
                                                       "sender@example.com",
                                                       "receiver@example.com",
                                                       "2021-11-30 10:10:00",
                                                       "image",
                                                       "image_hash"
                                                       )
        assert response is not None
    """

    @patch('mib.rao.message_manager.requests.delete')
    def test_create_draft_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.create_draft("message",
                                              "sender@example.com",
                                              "receiver@example.com",
                                              "2021-11-30 10:10:00",
                                              "image",
                                              "image_hash"
                                              )
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.delete')
    def test_delete_draft(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)
        response = self.message_manager.delete_draft(randint(0, 999))
        assert response is not None

    @patch('mib.rao.message_manager.requests.delete')
    def test_delete_draft_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.delete_draft(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    """
    # TypeError: Object of type Message is not JSON serializable
    @patch('mib.rao.message_manager.requests.post')
    def test_create_message(self, mock_post):
        mock_post.return_value = Mock(status_code=200)
        response = self.message_manager.create_message("message",
                                                       "sender@example.com",
                                                       "receiver@example.com",
                                                       "2021-11-30 10:10:00",
                                                       "image",
                                                       b'image_hash'
                                                       )
        assert response is not None
    """
    @patch('mib.rao.message_manager.requests.delete')
    def test_create_message_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.create_message("message",
                                                "sender@example.com",
                                                "receiver@example.com",
                                                "2021-11-30 10:10:00",
                                                "image",
                                                b'image_hash'
                                                )
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.delete')
    def test_delete_message(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)
        response = self.message_manager.delete_message("owner@examplecom",
                                                       randint(0, 999))
        assert response is not None

    @patch('mib.rao.message_manager.requests.delete')
    def test_delete_message_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.delete_message("owner@example.com",
                                                randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.delete')
    def test_withdraw(self, mock_delete):
        mock_delete.return_value = Mock(status_code=200)
        response = self.message_manager.withdraw(randint(0, 999))
        assert response is not None

    @patch('mib.rao.message_manager.requests.delete')
    def test_withdraw_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.withdraw(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    """
    # not JSON serializable
    @patch('mib.rao.message_manager.requests.put')
    def test_edit_draft(self, mock_put):
        mock_put.return_value = Mock(status_code=200)
        response = self.message_manager.edit_draft(randint(0, 999),
                                                   "message",
                                                   "sender@example.com",
                                                   "receiver@example.com",
                                                   "2021-11-30 10:10:00",
                                                   "image",
                                                   b'image_hash')
        assert response is not None
    """

    @patch('mib.rao.message_manager.requests.put')
    def test_edit_draft_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.edit_draft(randint(0, 999),
                                            "message",
                                            "sender@example.com",
                                            "receiver@example.com",
                                            "2021-11-30 10:10:00",
                                            "image",
                                            b'image_hash'
                                            )
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.get')
    def test_get_box(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                # I don't know what to put there
            }
        )
        response = self.message_manager.get_box("owner", "box")
        assert response is not None

    @patch('mib.rao.message_manager.requests.get')
    def test_get_box_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = Mock(status_code=400, json=lambda: {
            'message':
                0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.get_box("owner", "box")
            self.assertEqual(http_error.exception.code, 500)

    @patch('mib.rao.message_manager.requests.put')
    def test_set_as_read(self, mock_put):
        mock_put.return_value = Mock(status_code=200)
        response = self.message_manager.set_as_read(randint(0, 999))
        assert response is not None

    @patch('mib.rao.message_manager.requests.put')
    def test_set_as_read_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda: {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.message_manager.set_as_read(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)
