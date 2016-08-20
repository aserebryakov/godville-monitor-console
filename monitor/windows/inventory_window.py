import curses
from ..core import TiledWindow
from ..core import TextEntry
from ..core import Colors


class InventoryWindow(TiledWindow):
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

    def init_text_entries(self):
        self.text_entries.append(TextEntry('Gold', 'gold_approx', self.width))
        self.text_entries.append(TextEntry('Bricks', 'bricks_cnt', self.width))
        self.text_entries.append(TextEntry('Wood', 'wood_cnt', self.width))
        self.text_entries.append(TextEntry('Useful Items',
            lambda state: sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()]),
                                            self.width))
        self.text_entries.append(TextEntry('High Cost Items',
            lambda state: sum([(1 if item['price'] > 0 else 0) for item in state['inventory'].values()]),
                                            self.width))
        self.text_entries.append(TextEntry('Total Items',
                                           'inventory_num',
                                            self.width))

