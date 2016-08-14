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
