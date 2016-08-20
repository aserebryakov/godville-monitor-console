import curses
from ..core import TiledWindow
from ..core import TextEntry
from ..core import Colors


class QuestWindow(TiledWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        (parent_height, parent_width) = parent_window.getmaxyx()
        height = 8
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(QuestWindow, self).__init__('Quest',
                                          height,
                                          width,
                                          parent_window,
                                          top_window,
                                          left_window)

