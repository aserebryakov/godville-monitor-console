import curses
from core.monitor_window import MonitorWindow
from core.text_entry import TextEntry
from core.text_entry import Colors


class PetWindow(MonitorWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        height = 6
        width  = 22
        super(PetWindow, self).__init__('Pet',
                                        height,
                                        width,
                                        parent_window,
                                        top_window,
                                        left_window)

    def update(self, state):
        pet = state['pet']
        super(PetWindow, self).update(pet)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('', 'pet_class', self.width))
        self.text_entries.append(TextEntry('', 'pet_name', self.width))
        self.text_entries.append(TextEntry('Level', 'pet_level', self.width))

