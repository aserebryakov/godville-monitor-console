import pprint
import json
import time
from urllib.request import urlopen
import curses

class Colors:
    STANDART        = 1
    HEALTH_POINTS   = 2
    POWER_POINTS    = 3
    ATTENTION       = 4


class Monitor:
    def __init__(self):
        self.stdscr = curses.initscr()
        (self.stdscr_height, self.stdscr_width) = self.stdscr.getmaxyx()
        self.main_window = curses.newwin(self.stdscr_height, self.stdscr_width)

        curses.noecho()
        curses.cbreak()
        self.stdscr.clear()

        if curses.has_colors() == True:
            curses.start_color()
        self.init_colors()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def init_colors(self):
        curses.init_pair(Colors.STANDART, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Colors.HEALTH_POINTS, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Colors.POWER_POINTS, curses.COLOR_BLUE, curses.COLOR_BLACK)

    def main_loop(self):
        state = None
        previous_state = None

        while(True):
            connection = urlopen('http://godville.net/gods/api/GODNAME.json')
            state = json.loads(connection.read().decode('utf-8'))
            #pprint.pprint(state)
            self.main_window.addstr(10, 5, '{0}'.format(state['name']), curses.color_pair(Colors.STANDART))
            self.main_window.addstr(11, 5, 'HP {0}'.format(state['health']), curses.color_pair(Colors.HEALTH_POINTS))
            self.main_window.addstr(12, 5, 'Power {0}'.format(state['godpower']), curses.color_pair(Colors.POWER_POINTS))
            self.main_window.addstr(13, 5, 'Inventory items {0}'.format(len(state['inventory'])), curses.color_pair(Colors.STANDART))
            self.main_window.refresh()
            time.sleep(10)

def main():
    monitor = Monitor()
    monitor.main_loop()


if __name__ == '__main__':
    main()
