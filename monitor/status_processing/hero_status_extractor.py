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

        self.keys = ['name', 'health', 'max_health', 'godpower',
                     'exp_progress', 'town_name', 'distance', 'arena_fight']

        self.inspector.add_rule(Rule('health', '<', 40, 'Low Health'))
        self.inspector.add_rule(Rule('arena_fight',
                                     '==',
                                     True,
                                     'Hero is in fight'))
