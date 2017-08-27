import requests

from .registry import SmsHandlerRegistry


class SmsHandlerAbstract(metaclass=SmsHandlerRegistry):
    BASE_URL = None

    def get_url(self, *args, **kwargs):
        raise NotImplementedError

    def send(self, data, *args, **kwargs):
        response = requests.post(self.get_url(*args, **kwargs), data=data)
        try:
            response.raise_for_status()
            data = response.json()
            if data.get('status') == 'ok':
                self.log_success(data, response)
            else:
                self.log_fail(data, response)

        except requests.RequestException as exc:
            self.log_fail(data, response)

        except ValueError:
            self.log_error()

    def log_success(self, request_data, response):
        pass


    def log_fail(self, request_data, response):
        pass


    def log_error(self):
        pass