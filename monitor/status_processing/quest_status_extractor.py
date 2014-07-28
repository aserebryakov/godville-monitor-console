from .rule import Rule
from .info_extractor import InfoExtractor

class QuestStatusExtractor(InfoExtractor):
    '''
    Class extracting information about hero status
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(QuestStatusExtractor, self).__init__('quest_status')

        self.keys = ['quest', 'quest_progress', 'diary_last']

