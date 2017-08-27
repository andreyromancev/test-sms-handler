class SmsHandlerRegistry(type):
    BASE_NAME = 'SmsHandlerAbstract'

    registry = dict()

    def __init__(cls, name, bases, nmspc):
        super(SmsHandlerRegistry, cls).__init__(name, bases, nmspc)

        if SmsHandlerRegistry.BASE_NAME in [b.__name__ for b in bases]:
            SmsHandlerRegistry.registry[name] = cls()


def get_handler(name):
    return SmsHandlerRegistry.registry.get(name)