# coding=utf-8
import requests
from django.test import mock, TransactionTestCase

from ..models import RequestLog, RequestLogError
from ..handlers import get_handler


class SmsHandlerBaseTestMixin:
    HANDLER_NAME = None

    def setUp(self):
        super(SmsHandlerBaseTestMixin, self).setUp()

        self.handler = get_handler(self.HANDLER_NAME)
        self.response = mock.Mock()

    def test_makes_post_request_with_data(self):
        response = mock.Mock()
        response.json.return_value = {'status': 'ok', 'phone': 'any phone'}

        with mock.patch('requests.post', return_value=response) as post_mock:
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

    def test_success_log_creates_logs(self):
        url = 'test url'
        data = {'test_key': 'test_value'}
        response = mock.Mock()
        response.json.return_value = {'phone': 'any phone'}

        self.handler.log_success(url, data, response)
        self.assertTrue(RequestLog.objects.filter(
            url=url, request_data=data, phone='any phone',
        ).exists())

    def test_fail_log_creates_logs(self):
        url = 'test url'
        data = {'test_key': 'test_value'}
        response = mock.Mock()
        response.json.return_value = {
            'phone': 'any phone',
            'error_code': -3500,
            'error_msg': 'Невозможно отправить сообщение указанному абоненту',
        }

        self.handler.log_fail(url, data, response)
        self.assertTrue(RequestLog.objects.filter(
            url=url, request_data=data, phone='any phone',
        ).exists())
        self.assertTrue(RequestLogError.objects.filter(
            code=-3500, message='Невозможно отправить сообщение указанному абоненту',
        ).exists())

    def test_error_log_creates_logs(self):
        url = 'test url'
        data = {'test_key': 'test_value'}

        self.handler.log_error(url, data)
        self.assertTrue(RequestLog.objects.filter(
            url=url, request_data=data,
        ).exists())
        self.assertTrue(RequestLogError.objects.filter(
            message='Response parsing error',
        ).exists())


class SmsCenterTestCase(SmsHandlerBaseTestMixin, TransactionTestCase):
    HANDLER_NAME = 'SmsCenterHandler'


class SmsTrafficTestCase(SmsHandlerBaseTestMixin, TransactionTestCase):
    HANDLER_NAME = 'SmsTrafficHandler'
