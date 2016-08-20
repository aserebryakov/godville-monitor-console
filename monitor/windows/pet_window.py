import curses
from ..core import TiledWindow
from ..core import TextEntry
from ..core import Colors


class PetWindow(TiledWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        height = 6
        width  = 22
        super(PetWindow, self).__init__('Pet',
                                        height,
                                        width,
                                        parent_window,
                                        top_window,
                                        left_window)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('', lambda state: state['pet']['pet_class'], self.width))
        self.text_entries.append(TextEntry('', lambda state: state['pet']['pet_name'], self.width))
        self.text_entries.append(TextEntry('Level', lambda state: state['pet']['pet_level'], self.width))

