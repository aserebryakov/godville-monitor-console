from .rule import Rule
from .info_extractor import InfoExtractor

class HeroStatusExtractor(InfoExtractor):
    '''
    Class extracting information about hero status
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(HeroStatusExtractor, self).__init__('hero_status')
