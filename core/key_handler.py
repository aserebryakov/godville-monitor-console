import curses

class HandlerAlreadyRegisteredException(BaseException):
    pass

class KeyHandlingManager:
    def __init__(self):
        self._handlers = dict()

    def is_registered(self, key):
        pass

    def register_handler(self, key, handler):
        pass

    def handle_keys(self, keys):
        pass
