import curses
from core import TiledWindow
from core import TextEntry
from core import Colors


class ApplicationStatusWindow(TiledWindow):
    def __init__(self, parent_window, top_window = None, left_window = None):
        (height, width) = parent_window.getmaxyx()
        height = height - top_window.y - top_window.height
        super(ApplicationStatusWindow, self).__init__('Application Status',
                                                      height,
                                                      width,
                                                      parent_window,
                                                      top_window,
                                                      left_window)

    def update(self, state):
        try:
            # fictive access to the field
            state['expired']
            state['session_status'] = 'Session is expired'
        except KeyError as err:
            state['session_status'] = 'Session is active'

        super(ApplicationStatusWindow, self).update(state)

    def init_text_entries(self):
        self.text_entries.append(TextEntry('',
                                           'session_status',
                                           self.width))
