from .info_extractor import InfoExtractor

class PetStatusExtractor(InfoExtractor):
    '''
    Class extracting information about hero status
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(PetStatusExtractor, self).__init__('pet_status')

    def extract_info(self, status):
        '''
        Method extracting necessary info from status dictionary.
        returns dictionary of related elements
        '''
        pet = status['pet']
        super(PetStatusExtractor, self).extract_info(pet)

