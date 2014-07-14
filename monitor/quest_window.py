import curses
from core import TiledWindow
from core import TextEntry
from core import Colors


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

    def update(self, state):
        super(QuestWindow, self).update(state)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('', 'quest', self.width))
        self.text_entries.append(TextEntry('Progress, %',
                                           'quest_progress',
                                           self.width))

        self.text_entries.append(TextEntry('',
                                           '',
                                           self.width))

        self.text_entries.append(TextEntry('',
                                           'diary_last',
                                           self.width))
