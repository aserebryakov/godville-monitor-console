import logging
import curses
from .text_entry import TextEntry
from .monitor_window import MonitorWindowBase

class WarningWindow(MonitorWindowBase):
    def __init__(self,
                 parent_window,
                 text):

        self._text = text
        self._last_line = 'Press ENTER...'

        # Include borders to window size
        width  = max(len(self._text), len(self._last_line)) + 2
        height = 5

        (max_y, max_x) = parent_window.getmaxyx()

        y = int((max_y - height)/2)
        x = int((max_x - width)/2)

        if (x < 0 or y < 0):
            logging.error('%s: Warning text is too long \'%s\'',
                          self.__init__.__name__,
                          self._text)
            x = 0
            y = 0

        super(WarningWindow, self).__init__('Warning',
                                            height,
                                            width,
                                            parent_window,
                                            y,
                                            x)

    def init_text_entries(self):
        self.text_entries.append(TextEntry(self._text, '', self.width))
        self.text_entries.append(TextEntry(self._last_line, '', self.width))
