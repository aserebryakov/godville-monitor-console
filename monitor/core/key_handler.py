import curses
import logging


class HandlerAlreadyRegisteredException(Exception):
    def __init__(self):
        message = 'This key is already registered'
        super(HandlerAlreadyRegisteredException, self).__init__(self, message)


class KeyHandlingManager:
    def __init__(self):
        self._handlers = dict()

    def is_registered(self, key):
        result = (key in self._handlers.keys())
        logging.debug('%s: Checking key \'%s\', result is %s',
                      self.is_registered.__name__,
                      key,
                      str(result))

        return result

    def register_handler(self, key, handler):
        logging.debug('%s: Registering key \'%s\'',
                      self.register_handler.__name__,
                      key)

        if self.is_registered(key) != True:
            self._handlers[key] = handler
        else:
            raise HandlerAlreadyRegisteredException()

    def handle_key(self, key):
        logging.debug('%s: Handling key \'%s\'',
                      self.handle_key.__name__,
                      key)

        if self.is_registered(key) == True:
            return self._handlers[key]()
