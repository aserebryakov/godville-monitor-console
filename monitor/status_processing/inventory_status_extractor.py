from .rule import Rule
from .info_extractor import InfoExtractor

class InventoryStatusExtractor(InfoExtractor):
    '''
    Class extracting information about hero status
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(InventoryStatusExtractor, self).__init__('inventory_status')

        self.keys = ['bricks_cnt', 'wood_cnt', 'inventory_num', 'inventory']

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        returns dictionary of related elements
        '''
        super(InventoryStatusExtractor, self).extract_info(status)

        active_items    = 0
        high_cost_items = 0

        # TODO: add items processing

        self.info['active_items']    = active_items
        self.info['high_cost_items'] = high_cost_items
