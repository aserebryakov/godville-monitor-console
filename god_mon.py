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
        window - Reference to curses window object

    Methods:
        update(state) - Virtual method to update window with a given state
                        Must be implemented for each derived class
    '''

    def __init__(self, parent_window, top_window, left_window, height, width):
        self._top_window  = top_window
        self._left_window = left_window

        if top_window != None:
            self._y           = top_window.y + top_window.height + 1
        else:
            self._y           = 1

        if left_window != None:
            self._x           = left_window.x + left_window.width + 1
        else:
            self._x           = 1

        self._height      = height
        self._width       = width
        self._window      = parent_window.subwin(self.height, self.width, self.y, self.x)
        self._window.box()

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

    def update(self, state):
        assert(False, 'Not implemented')

    def add_strings(self, string_list):
        for i, string in enumerate(string_list):
            self._window.addstr(i + 1,
                                1,
                                string[0],
                                curses.color_pair(string[1]))

class StatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 20
        width  = 15
        super(StatusWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'State')

        state_text = [ (state['name'], Colors.STANDART),
                       ('HP    {0}/{1}'.format(state['health'],
                                            state['max_health']),
                        Colors.HEALTH_POINTS),
                       ('Power    {0}%'.format(state['godpower']),
                         Colors.POWER_POINTS),
                       ('Level    {0}'.format(state['level']),
                         Colors.STANDART),
                       ('EXP      {0}%'.format(state['exp_progress']),
                        Colors.STANDART),
                       ('Town {0}'.format(state['town_name']),
                        Colors.STANDART),
                       ('Distance {0}'.format(state['distance']),
                        Colors.STANDART) ]

        self.add_strings(state_text)

class QuestWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (parent_height, parent_width) = parent_window.getmaxyx()
        height = 6
        width  = parent_height - left_window.x + left_window.width - 1
        super(QuestWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Quest')

        state_text = [ ('{0}'.format(state['quest']),
                        Colors.STANDART),
                       ('Progress {0}'.format(state['quest_progress']),
                        Colors.STANDART),
                       ('Field news:',
                        Colors.STANDART) ]

        self.add_strings(state_text)

    def split_diary_last(self, diary_last, lenght):
        words = diary_last.split(' ', diary_last)
        lines = []

        for i in range(len(words)):
            current_line = ''

            while(len(current_line) < (level - words[i])):
                current_line = current_line + ' ' + words[i]

            lines.append(current_line)

        return lines


class MainWindow(MonitorWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__(stdscr, None, None, height - 2 , width - 2)

        self._subwindows = []
        self._subwindows.append(StatusWindow(self.window, None, None))
        self._subwindows.append(QuestWindow(self.window, None, self._subwindows[-1]))

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
            state = self.read_form_url('http://godville.net/gods/api/{0}.json'.format(self.godname))
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
