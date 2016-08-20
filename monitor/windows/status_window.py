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

