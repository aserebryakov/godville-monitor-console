import logging
import curses

class MonitorWindow:
    '''
    Base class for all windows of the Godville Monitor

    '''
    def __init__(self,
                 title,
                 height,
                 width,
                 parent_window,
                 top_window = None,
                 left_window = None,
                 y = 0,
                 x = 0):

        self._title        = title
        self._top_window   = top_window
        self._left_window  = left_window
        self._text_entries = []

        if top_window != None:
            self._y           = top_window.y + top_window.height
        else:
            self._y           = y

        if left_window != None:
            self._x           = left_window.x + left_window.width
        else:
            self._x           = x

        self._height      = height
        self._width       = width
        self._window      = parent_window.subwin(self.height,
                                                 self.width,
                                                 self.y,
                                                 self.x)
        self._window.box()
        self.init_text_entries()

    @property
    def top_window(self):
        return self._top_window

    @property
    def left_window(self):
        return self._left_window

    @property
    def window(self):
        return self._window

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def title(self):
        return self._title

    @property
    def text_entries(self):
        return self._text_entries

    def add_text_entry(self, entry):
        self.text_entries.append(entry)

    def update(self, state):
        logging.debug('%s: Updating window \'%s\'',
                      self.update.__name__,
                      self.title)

        self.window.clear()
        self.window.box()
        self._window.addstr(0, 2, self.title)

        for entry in self.text_entries:
            entry.update(state)

        self.write_text(self.text_entries)
        self.window.refresh()

    def init_text_entries(self):
        pass

    def write_text(self, entries):
        for i, entry in enumerate(entries):
            logging.debug('%s: Writting text \'%s\'',
                          self.write_text.__name__,
                          entry.text)

            self._window.addstr(i + 1,
                                1,
                                entry.text,
                                curses.color_pair(entry.color))

