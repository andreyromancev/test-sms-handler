from .registry import SmsHandlerRegistry


class SmsHandlerAbstract(metaclass=SmsHandlerRegistry):
    pass
