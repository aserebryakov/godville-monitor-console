import curses
from core.monitor_window import MonitorWindow
from core.text_entry import TextEntry
from core.text_entry import Colors


class QuestWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (parent_height, parent_width) = parent_window.getmaxyx()
        height = 8
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(QuestWindow, self).__init__('Quest',
                                          parent_window,
                                          top_window,
                                          left_window,
                                          height,
                                          width)

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
