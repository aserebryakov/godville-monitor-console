import pprint
import json
import time
from urllib.request import urlopen
import curses
import argparse

class Colors:
    STANDART        = 1
    HEALTH_POINTS   = 2
    POWER_POINTS    = 3
    ATTENTION       = 4


class MonitorWindow:
    '''
    Base class for all windows of the Godville Monitor

    Properties:
        window      - reference to curses window object
        top_window  - reference to window placed above
        left_window - reference to window placed on the left
        x           - x coordinate of the window
        y           - y coordinate of the window
        width       - window width
        height      - window height

    Methods:
        update(state) - Virtual method to update window with a given state
                        Must be implemented for each derived class

        write_text(string_list) - writes all the lines in argument to a window
    '''

    def __init__(self, parent_window, top_window, left_window, height, width):
        self._top_window   = top_window
        self._left_window  = left_window
        self._text_entries = []

        if top_window != None:
            self._y           = top_window.y + top_window.height
        else:
            self._y           = 0

        if left_window != None:
            self._x           = left_window.x + left_window.width
        else:
            self._x           = 0

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
    def text_entries(self):
        return self._text_entries

    def add_text_entry(self, entry):
        self.text_entries.append(entry)

    def update(self, state):
        self.window.clear()
        self.window.box()

        for entry in self.text_entries:
            entry.update(state)

        self.write_text(self.text_entries)
        self.window.refresh()

    def init_text_entries(self):
        pass

    def write_text(self, entries):
        for i, entry in enumerate(entries):
            self._window.addstr(i + 1,
                                1,
                                entry.text,
                                curses.color_pair(entry.color))


class TextEntry:
    def __init__(self, predefined_text, key, width, color = Colors.STANDART):
        self._predefined_text = predefined_text
        self._key             = key
        self._width           = width
        self._color           = color
        self._attribute       = None
        self._text            = ''

    @property
    def predefined_text(self):
        return self._predefined_text

    @property
    def width(self):
        return self._width

    @property
    def key(self):
        return self._key

    @property
    def text(self):
        return self._text

    @property
    def text(self):
        return self._text

    @property
    def color(self):
        return self._color

    @property
    def attribute(self):
        return self._attribute

    @property
    def attribute(self, attribute):
        self._attribute = attribute

    def update(self, state, attribute = None):
        key_width   = self.width - len(self.predefined_text) - 2
        custom_text = ''

        if self.key == '':
            self._text = ''
            return

        try:
            custom_text = '{0}'.format(state[self.key])
        except KeyError:
            self._text = '{0} key not found'.format(self.key)
            return

        if key_width < 1:
            self._text = '{0} text doesn\'t fit'.format(key)
            return

        self._text = '{0}{1:>{2}}'.format(self.predefined_text,
                                          custom_text,
                                          key_width)


class StatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 10
        width  = 22
        super(StatusWindow, self).__init__(parent_window,
                                           top_window,
                                           left_window,
                                           height,
                                           width)

    def update(self, state):
        super(StatusWindow, self).update(state)
        self._window.addstr(0, 2, 'Status')

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


class PetWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 6
        width  = 22
        super(PetWindow, self).__init__(parent_window,
                                        top_window,
                                        left_window,
                                        height,
                                        width)

    def update(self, state):
        pet = state['pet']
        super(PetWindow, self).update(pet)
        self._window.addstr(0, 2, 'Pet')

    def init_text_entries(self):
        self.text_entries.append(TextEntry('', 'pet_class', self.width))
        self.text_entries.append(TextEntry('', 'pet_name', self.width))
        self.text_entries.append(TextEntry('Level', 'pet_level', self.width))


class QuestWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (parent_height, parent_width) = parent_window.getmaxyx()
        height = 8
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(QuestWindow, self).__init__(parent_window,
                                          top_window,
                                          left_window,
                                          height,
                                          width)

    def update(self, state):
        super(QuestWindow, self).update(state)
        self._window.addstr(0, 2, 'Quest')

    def init_text_entries(self):
        self.text_entries.append(TextEntry('Quest:', 'quest', self.width))
        self.text_entries.append(TextEntry('Progress, %',
                                           'quest_progress',
                                           self.width))

        self.text_entries.append(TextEntry('',
                                           '',
                                           self.width))

        self.text_entries.append(TextEntry('',
                                           'diary_last',
                                           self.width))



class InventoryWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 8
        (parent_height, parent_width) = parent_window.getmaxyx()
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(InventoryWindow, self).__init__(parent_window,
                                              top_window,
                                              left_window,
                                              height,
                                              width)

    def update(self, state):
        super(InventoryWindow, self).update(state)
        self._window.addstr(0, 2, 'Inventory')

    def init_text_entries(self):
        self.text_entries.append(TextEntry('Bricks', 'bricks_cnt', self.width))
        self.text_entries.append(TextEntry('Wood', 'wood_cnt', self.width))
        self.text_entries.append(TextEntry('Inventory Items',
                                           'inventory_num',
                                            self.width))

class ApplicationStatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (height, width) = parent_window.getmaxyx()
        height = height - top_window.y - top_window.height
        super(ApplicationStatusWindow, self).__init__(parent_window,
                                                      top_window,
                                                      left_window,
                                                      height,
                                                      width)

    def update(self, state):
        try:
            # fictive access to the field
            state['expired']
            state['session_status'] = 'expired'
        except KeyError as err:
            state['session_status'] = 'active'

        super(ApplicationStatusWindow, self).update(state)
        self._window.addstr(0, 2, 'Application Status')

    def init_text_entries(self):
        self.text_entries.append(TextEntry('Session is',
                                           'session_status',
                                           self.width))

class MainWindow(MonitorWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__(stdscr, None, None, height, width)

        self._subwindows = []

        statusWindow    = StatusWindow(self.window, None, None)
        questWindow     = QuestWindow(self.window, None, statusWindow)
        petWindow       = PetWindow(self.window, statusWindow, None)
        inventoryWindow = InventoryWindow(self.window,
                                          questWindow,
                                          statusWindow)

        applicationStatusWindow = ApplicationStatusWindow(self.window,
                                                          petWindow,
                                                          None)

        self._subwindows.append(statusWindow)
        self._subwindows.append(questWindow)
        self._subwindows.append(petWindow)
        self._subwindows.append(inventoryWindow)
        self._subwindows.append(applicationStatusWindow)

    def update(self, state):
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()


class Monitor:
    def __init__(self, args):
        self.init_windows()
        self.godname = args.god_name
        self.dump_file = args.dump

        curses.noecho()
        curses.cbreak()

        if curses.has_colors() == True:
            curses.start_color()
        self.init_colors()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def init_windows(self):
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.main_window = MainWindow(self.stdscr)

    def init_colors(self):
        curses.init_pair(Colors.STANDART,
                         curses.COLOR_WHITE,
                         curses.COLOR_BLACK)

        curses.init_pair(Colors.HEALTH_POINTS,
                         curses.COLOR_RED,
                         curses.COLOR_BLACK)

        curses.init_pair(Colors.POWER_POINTS,
                         curses.COLOR_BLUE,
                         curses.COLOR_BLACK)

    def read_state(self):
        state = None
        if self.dump_file != None:
            state = self.read_dump(self.dump_file).decode('utf-8')
        else:
            state = self.read_form_url('http://godville.net/gods/api/{0}.json'
                                       .format(self.godname))
        return state

    def read_form_url(self, url):
        connection = urlopen(url)
        return connection.read().decode('utf-8')

    def read_dump(self, dumpfile):
        state = None
        try:
            f = open(dumpfile, 'rb')
            state = f.read()
            f.close()
        except:
            print('Error occured')

        return state

    def main_loop(self):
        state = None
        previous_state = None

        while(True):
            state = json.loads(self.read_state())
            self.main_window.update(state)
            time.sleep(10)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('god_name',
                        help = 'Name of the god to me monitored')

    parser.add_argument('-d',
                        '--dump',
                        type = str,
                        help = 'read state from the dump (debug option)')

    args = parser.parse_args()

    monitor = Monitor(args)
    monitor.main_loop()


if __name__ == '__main__':
    main()
