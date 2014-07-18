class Rule:
    '''
    Class describing how to process dictinary item
    '''
    def __init__(self, key, condition, ethalon, message):
        self._key       = key
        self._condition = condition
        self._ethanlon  = ethanlon
        self._message   = message

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
        Checks if condition is satisfied
        '''
        pass

