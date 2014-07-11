#/bin/python3

import sys
import time
import argparse
import json
import curses
import logging
from urllib.request import urlopen

from core import Colors
from core import Timer
from core import KeyHandlingManager
from monitor import MainWindow

class KeyHandler:

    @staticmethod
    def quit():
        sys.exit()


class Monitor:
    def __init__(self, args):
        self.key_manager = KeyHandlingManager()
        self.init_windows()
        self.godname = args.god_name
        self.dump_file = args.dump

        curses.noecho()
        curses.cbreak()

        if curses.has_colors() == True:
            curses.start_color()

        self.init_colors()
        self.init_keys()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def init_keys(self):
        self.key_manager.register_handler('q', KeyHandler.quit)

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
        logging.debug('%s: reading state',
                      self.read_state.__name__)

        state = None

        try:
            if self.dump_file != None:
                state = self.read_dump(self.dump_file).decode('utf-8')
            else:
                state = self.read_form_url('http://godville.net/gods/api/{0}.json'
                                           .format(self.godname))
        except Exception as e:
            logging.error('%s: reading state error \n %s',
                          self.read_state.__name__,
                          str(e))
            print('Error occured, please see the pygod.log')

            sys.exit()

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

    def handle_key(self):
        key = self.stdscr.getkey()

        if key != '':
            self.key_manager.handle_key(key)

    def main_loop(self):
        timer = Timer(60)
        state = json.loads(self.read_state())
        self.main_window.update(state)

        while(True):
            if timer.expired():
                state = json.loads(self.read_state())
                self.main_window.update(state)
                timer.reset()
            self.handle_key()
            time.sleep(0.1)


def main():
    # Parsing arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('god_name',
                        help = 'Name of the god to me monitored')

    parser.add_argument('-d',
                        '--dump',
                        type = str,
                        help = 'read state from the dump (debug option)')

    args = parser.parse_args()

    # Configuring logs
    logging.basicConfig(filename='pygod.log', filemode='w+', level=logging.DEBUG)
    logging.debug('Starting PyGod with username %s', args.god_name)

    monitor = Monitor(args)
    monitor.main_loop()


if __name__ == '__main__':
    main()
