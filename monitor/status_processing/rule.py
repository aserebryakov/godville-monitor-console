import logging

class Rule:
    '''
    Class describing how to process dictinary item
    '''

    __allowed_conditions = ['<', '<=', '==', '!=', '>=', '>']

    def __init__(self, key, condition, ethalon, message):
        self._key         = key
        self._condition   = condition
        self._ethalon     = ethalon
        self._message     = message
        self._last_result = False

    @property
    def key(self):
        return self._key

    @property
    def condition(self):
        return self._condition

    @property
    def ethalon(self):
        return self._ethalon

    @property
    def message(self):
        return self._message

    def to_string(self):
        string = 'key = {0}, condition = {1}, ethalon = {2}, message = {3}'.\
                 format(self.key, self.condition, ethalon, self.message)

    def check(self, value):
        '''
        Checks if condition is satisfied and last result was False
        '''
        if ((type(value) is not int) and (type(value) is not bool)):
            logging.error('%s: incorrect value type %s',
                          self.check.__name__,
                          str(type(value)))
            return False

        if ((type(self.ethalon) is not int) and (type(self.ethalon) is not bool)):
            logging.error('%s: incorrect ethalon type %s',
                          self.check.__name__,
                          str(type(self.ethalon)))
            return False

        if self.condition not in self.__allowed_conditions:
            logging.error('%s: incorrect condition %s',
                          self.check.__name__,
                          str(type(self.condition)))
            return False

        result = eval(str(value) + str(self.condition) + str(self.ethalon))

        if self._last_result != result:
            self._last_result = result
            return result

        return False

