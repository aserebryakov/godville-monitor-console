from .dictionary_checker import DictionaryChecker

class InfoExtractor:
    '''
    Base class for all information extractors
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        self._inspector = DictionaryChecker()
        self._name      = name
        self._keys      = []
        self._messages  = []
        self._info      = {}

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        Should return dictionary of related elements
        '''
        for key in self.keys:
            try:
                self.info[key] = status[key]
            except KeyError:
                self.info[key] = 'N/A'

    def inspect_info(self):
        '''
        Function checking info with rules
        '''
        self.messages = self.inspector.check_rules(self.info)


    @property
    def inspector(self):
        '''
        Object checking state with rules
        '''
        return self._inspector

    @property
    def name(self):
        '''
        Inspector name
        '''
        return self._name

    @property
    def keys(self):
        '''
        List of keys of the related info
        '''
        return self._keys

    @keys.setter
    def keys(self, keys):
        '''
        List of keys of the related info
        '''
        self._keys = keys

    @property
    def messages(self):
        '''
        List of messages returned by the inspector
        '''
        return self._messages

    @messages.setter
    def messages(self, messages):
        '''
        List of messages returned by the inspector
        '''
        self._messages = messages

    @property
    def info(self):
        '''
        Info extracted from the dictionary
        '''
        return self._info

