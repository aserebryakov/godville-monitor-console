import logging
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

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        returns dictionary of related elements
        '''
        super(InventoryStatusExtractor, self).extract_info(status)

        active_items    = 0
        high_cost_items = 0

        for item in self.info['inventory'].values():
            logging.debug('%s: item %s',
                          self.extract_info.__name__,
                          str(item))

            if item['price'] > 0:
                high_cost_items += 1

            if 'activate_by_user' in item.keys():
                active_items += 1

        self.info['active_items']    = active_items
        self.info['high_cost_items'] = high_cost_items
