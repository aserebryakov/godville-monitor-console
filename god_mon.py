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
        (self.stdscr_height, self.stdscr_width) = self.stdscr.getmaxyx()
        self.stdscr.clear()

        self.main_window = curses.newwin(self.stdscr_height, self.stdscr_width)
        self.main_window.box()
        (height, width) = self.main_window.getmaxyx()
        self.status_window = self.main_window.subwin(20, 20, 1, 1)
        self.status_window.box()

    def init_colors(self):
        curses.init_pair(Colors.STANDART, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Colors.HEALTH_POINTS, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Colors.POWER_POINTS, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def update_state_window(self, state):
        self.status_window.addstr(0, 7, 'State')
        self.status_window.addstr(1, 1, '{0}'.format(state['name']), curses.color_pair(Colors.STANDART))
        self.status_window.addstr(2, 1, 'HP {0}'.format(state['health']), curses.color_pair(Colors.HEALTH_POINTS))
        self.status_window.addstr(3, 1, 'Power {0}'.format(state['godpower']), curses.color_pair(Colors.POWER_POINTS))
        self.status_window.addstr(4, 1, 'Inventory items {0}'.format(len(state['inventory'])), curses.color_pair(Colors.STANDART))

    def read_state(self):
        state = None
        if self.dump_file != None:
            state = self.read_dump(self.dump_file).decode('utf-8')
        else:
            state = self.read_form_url('http://godville.net/gods/api/{0}.json'.format(self.godname))
        #pprint.pprint(state)
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
            self.update_state_window(state)
            self.main_window.refresh()
            time.sleep(10)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('god_name', help = 'Name of the god to me monitored')
    parser.add_argument('-d', '--dump', type=str, help = 'read state from the dump (debug option)')
    args = parser.parse_args()

    monitor = Monitor(args)
    monitor.main_loop()


if __name__ == '__main__':
    main()
