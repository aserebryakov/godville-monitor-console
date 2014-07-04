import curses


class HandlerAlreadyRegisteredException(Exception):
    def __init__(self):
        message = 'This key is already registered'
        super(HandlerAlreadyRegisteredException, self).__init__(self, message)


class KeyHandlingManager:
    def __init__(self):
        self._handlers = dict()

    def is_registered(self, key):
        return (key in self._handlers.keys())

    def register_handler(self, key, handler):
        if self.is_registered(key) != True:
            self._handlers[key] = handler
        else:
            raise HandlerAlreadyRegisteredException()

    def handle_key(self, key):
        if self.is_registered(key) == True:
            return self._handlers[key]()
