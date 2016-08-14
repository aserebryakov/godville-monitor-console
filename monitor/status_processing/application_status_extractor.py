from .rule import Rule
from .info_extractor import InfoExtractor

class ApplicationStatusExtractor(InfoExtractor):
    '''
    Class extracting information about hero status
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ApplicationStatusExtractor, self).__init__('application_status')

        self.rules.append(Rule(
            lambda info: 'expired' in info and info['expired'],
            lambda: self.messages.append('Session is expired. Please reconnect.')
            ))

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        Should return dictionary of related elements
        '''
        if 'expired' in status.keys():
            self.info['session_status'] = 'Session is expired'
            self.info['expired'] = True
        else:
            self.info['session_status'] = 'Session is active'
            self.info['expired'] = False
