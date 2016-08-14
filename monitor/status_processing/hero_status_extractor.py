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

        self.rules.append(Rule(
            lambda info: 'health' in info and info['health'] < 40,
            lambda: self.messages.append('Low Health')
            ))
        self.rules.append(Rule(
            lambda info: 'arena_fight' in info and info['arena_fight'],
            lambda: self.messages.append('Hero is in fight')
            ))
