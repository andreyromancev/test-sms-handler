import requests

from .registry import SmsHandlerRegistry
from .models import RequestLog, RequestLogError


class SmsHandlerAbstract(metaclass=SmsHandlerRegistry):
    BASE_URL = None

    def get_url(self, *args, **kwargs):
        raise NotImplementedError

    def send(self, data, *args, **kwargs):
        url = self.get_url(*args, **kwargs)
        response = requests.post(url, data=data)
        try:
            response.raise_for_status()
            data = response.json()
            if data.get('status') == 'ok':
                self.log_success(url, data, response)
            else:
                self.log_fail(url, data, response)

        except requests.RequestException:
            self.log_fail(url, data, response)

        except ValueError:
            self.log_error(url, data)

    def log_success(self, url, request_data, response):
        response_data = response.json()
        RequestLog.objects.create(
            url=url,
            request_data=request_data,
            phone=response_data.get('phone'),
        )

    def log_fail(self, url, request_data, response):
        response_data = response.json()
        log = RequestLog.objects.create(
            url=url,
            request_data=request_data,
            phone=response_data.get('phone'),
        )
        RequestLogError.objects.create(
            log=log,
            code=response_data.get('error_code'),
            message=response_data.get('error_msg'),
        )

    def log_error(self, url, request_data):
        log = RequestLog.objects.create(
            url=url,
            request_data=request_data,
        )
        RequestLogError.objects.create(
            log=log,
            message='Response parsing error',
        )
