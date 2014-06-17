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
        self._top_window  = top_window
        self._left_window = left_window

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

    def write_text(self, string_list):
        for i, string in enumerate(string_list):
            self._window.addstr(i + 1,
                                1,
                                string[0],
                                curses.color_pair(string[1]))

class StatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 10
        width  = 22
        super(StatusWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Status')

        state_text = [ (state['name'], Colors.STANDART),
                       ('HP{0:>14}/{1}'.format(state['health'],
                                               state['max_health']),
                        Colors.HEALTH_POINTS),
                       ('Power{0:>14}%'.format(state['godpower']),
                         Colors.POWER_POINTS),
                       ('Level{0:>15}'.format(state['level']),
                         Colors.STANDART),
                       ('EXP{0:>16}%'.format(state['exp_progress']),
                        Colors.STANDART),
                       ('Town{0:>15}'.format(state['town_name']),
                        Colors.STANDART),
                       ('Distance{0:>12}'.format(state['distance']),
                        Colors.STANDART) ]

        self.write_text(state_text)


class PetWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 6
        width  = 22
        super(PetWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Pet')

        pet = state['pet']

        state_text = [ ('{0:^20}'.format(pet['pet_class']),
                         Colors.STANDART),
                       ('{0:^20}'.format(pet['pet_name']), Colors.STANDART),
                       ('Level{0:>14}'.format(pet['pet_level']),
                         Colors.STANDART) ]

        self.write_text(state_text)

class QuestWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (parent_height, parent_width) = parent_window.getmaxyx()
        height = 8
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(QuestWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Quest')

        state_text = [ ('{0}'.format(state['quest']),
                        Colors.STANDART),
                       ('Progress {0}'.format(state['quest_progress']),
                        Colors.STANDART),
                       ('Field news:',
                        Colors.STANDART),
                       (state['diary_last'],
                        Colors.STANDART) ]

        self.write_text(state_text)

    def split_diary_last(self, diary_last, lenght):
        words = diary_last.split(' ', diary_last)
        lines = []

        for i in range(len(words)):
            current_line = ''

            while(len(current_line) < (level - words[i])):
                current_line = current_line + ' ' + words[i]

            lines.append(current_line)

        return lines


class InventoryWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 8
        (parent_height, parent_width) = parent_window.getmaxyx()
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(InventoryWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Inventory')

        state_text = [ ('Bricks{0:>14}'.format(state['bricks_cnt']),
                         Colors.STANDART),
                       ('Wood{0:>14}'.format(state['wood_cnt']),
                         Colors.STANDART),
                       ('Inventory {0:>10}/{1}'.format(state['inventory_num'],
                                                       state['inventory_max_num']),
                         Colors.STANDART) ]

        self.write_text(state_text)


class ApplicationStatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        (height, width) = parent_window.getmaxyx()
        height = height - top_window.y - top_window.height
        super(ApplicationStatusWindow, self).__init__(parent_window, top_window, left_window, height, width)

    def update(self, state):
        self._window.addstr(0, 2, 'Application Status')

        sessionExpired = ''

        try:
            sessionExpired = 'Session is expired'
        except KeyError as err:
            sessionExpired = 'Session is active'

        state_text = [ ( sessionExpired, Colors.STANDART) ]

        self.write_text(state_text)


class MainWindow(MonitorWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__(stdscr, None, None, height, width)

        self._subwindows = []

        statusWindow    = StatusWindow(self.window, None, None)
        questWindow     = QuestWindow(self.window, None, statusWindow)
        petWindow       = PetWindow(self.window, statusWindow, None)
        inventoryWindow = InventoryWindow(self.window, questWindow, statusWindow)
        applicationStatusWindow = ApplicationStatusWindow(self.window, petWindow, None)

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
