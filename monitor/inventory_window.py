import curses
from core.monitor_window import MonitorWindow
from core.text_entry import TextEntry
from core.text_entry import Colors


class InventoryWindow(MonitorWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        height = 8
        (parent_height, parent_width) = parent_window.getmaxyx()
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(InventoryWindow, self).__init__('Inventory',
                                              height,
                                              width,
                                              parent_window,
                                              top_window,
                                              left_window)

    def update(self, state):
        super(InventoryWindow, self).update(state)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('Bricks', 'bricks_cnt', self.width))
        self.text_entries.append(TextEntry('Wood', 'wood_cnt', self.width))
        self.text_entries.append(TextEntry('Inventory Items',
                                           'inventory_num',
                                            self.width))
