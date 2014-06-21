import pprint
import json
import time
from urllib.request import urlopen
import curses
import argparse
from monitor_window import MonitorWindow
from text_entry import TextEntry
from text_entry import Colors


class StatusWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 10
        width  = 22
        super(StatusWindow, self).__init__('Status',
                                           parent_window,
                                           top_window,
                                           left_window,
                                           height,
                                           width)

    def update(self, state):
        super(StatusWindow, self).update(state)

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
        super(PetWindow, self).__init__('Pet',
                                        parent_window,
                                        top_window,
                                        left_window,
                                        height,
                                        width)

    def update(self, state):
        pet = state['pet']
        super(PetWindow, self).update(pet)

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



class InventoryWindow(MonitorWindow):
    def __init__(self, parent_window, top_window, left_window):
        height = 8
        (parent_height, parent_width) = parent_window.getmaxyx()
        width  = parent_width

        if left_window != None:
            width = width - left_window.x - left_window.width

        super(InventoryWindow, self).__init__('Inventory',
                                              parent_window,
                                              top_window,
                                              left_window,
                                              height,
                                              width)

    def update(self, state):
        super(InventoryWindow, self).update(state)

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
        super(ApplicationStatusWindow, self).__init__('Application Status',
                                                      parent_window,
                                                      top_window,
                                                      left_window,
                                                      height,
                                                      width)

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

class MainWindow(MonitorWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__('', stdscr, None, None, height, width)

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
