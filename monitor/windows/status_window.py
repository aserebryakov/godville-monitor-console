import curses
from ..core import TiledWindow
from ..core import TextEntry
from ..core import Colors


class StatusWindow(TiledWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        height = 10
        width  = 22
        super(StatusWindow, self).__init__('Status',
                                           height,
                                           width,
                                           parent_window,
                                           top_window,
                                           left_window)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('', 'name', self.width))
        self.text_entries.append(TextEntry('HP',
                                           'health',
                                           self.width,
                                           Colors.HEALTH_POINTS))

        self.text_entries.append(TextEntry('Max HP',
                                           'max_health',
                                           self.width,
                                           Colors.HEALTH_POINTS))

        self.text_entries.append(TextEntry('Power, %',
                                           'godpower',
                                           self.width,
                                           Colors.POWER_POINTS))

        self.text_entries.append(TextEntry('EXP, %',
                                           'exp_progress',
                                           self.width))

        self.text_entries.append(TextEntry('Town', 'town_name', self.width))
        self.text_entries.append(TextEntry('Distance', 'distance', self.width))


    def update(self, state):
        super(StatusWindow, self).update(state)
