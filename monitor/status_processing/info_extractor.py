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
        self.messages  = []
        self.info      = {}

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        Should return dictionary of related elements
        '''
        self.info = status

    def inspect_info(self):
        '''
        Function checking info with rules
        '''
        self.messages = []

        for rule in self.rules:
            rule.check(self.info)


