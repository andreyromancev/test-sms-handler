from .base import SmsHandlerAbstract


class SmsCenterHandler(SmsHandlerAbstract):
    BASE_URL = 'http://smsc.ru/some­api/message/'

    def get_url(self, *args, **kwargs):
        return self.BASE_URL



class SmsTrafficHandler(SmsHandlerAbstract):
    BASE_URL = 'http://smstraffic.ru/super­api/message/'

    def get_url(self, *args, **kwargs):
        return self.BASE_URL