import logging

class InfoExtractor:
    '''
    Base class for all information extractors
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self.rules = []
        self.name      = name
        self.keys      = []
        self.messages  = []
        self.info      = {}

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        Should return dictionary of related elements
        '''
        for key in self.keys:
            try:
                self.info[key] = status[key]
            except KeyError:
                logging.warning('%s: key is not found %s',
                                self.extract_info.__name__,
                                key)
                self.info[key] = 'N/A'

    def inspect_info(self):
        '''
        Function checking info with rules
        '''
        self.messages = []

        for rule in self.rules:
            rule.check(self.info)


