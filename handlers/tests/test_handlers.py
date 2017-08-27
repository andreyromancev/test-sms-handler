import requests
from django.test import mock, TransactionTestCase

from ..registry import get_handler


class SmsHandlerBaseTestCase(TransactionTestCase):
    HANDLER_NAME = None

    def setUp(self):
        super(SmsHandlerBaseTestCase, self).setUp()

        self.handler = get_handler(self.HANDLER_NAME)
        self.response = mock.Mock()

    @mock.patch('requests.post', return_value=mock.Mock())
    def test_makes_post_request_with_data(self, post_mock):
        data = {'test_key': 'test_value'}
        self.handler.send(data)

        post_mock.assert_called_with(self.handler.get_url(), data=data)

    def test_calls_success_log_on_success(self):
        response = mock.Mock()
        response.json.return_value = {'status': 'ok'}

        with mock.patch('requests.post', return_value=response):
            with mock.patch.object(self.handler, 'log_success') as log_success:
                self.handler.send({})
                log_success.assert_called()

    def test_calls_fail_log_on_fail(self):
        response = mock.Mock()
        response.raise_for_status.side_effect = requests.RequestException

        with mock.patch('requests.post', return_value=response):
            with mock.patch.object(self.handler, 'log_fail') as log_fail:
                self.handler.send({})
                log_fail.assert_called()

    def test_calls_error_log_on_error(self):
        response = mock.Mock()
        response.raise_for_status.side_effect = ValueError

        with mock.patch('requests.post', return_value=response):
            with mock.patch.object(self.handler, 'log_error') as log_error:
                self.handler.send({})
                log_error.assert_called()


class SmsCenterTestCase(SmsHandlerBaseTestCase):
    HANDLER_NAME = 'SmsCenterHandler'


class SmsTrafficTestCase(SmsHandlerBaseTestCase):
    HANDLER_NAME = 'SmsTrafficHandler'
