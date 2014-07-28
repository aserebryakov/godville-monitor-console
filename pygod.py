#!/usr/bin/python3

import sys
import time
import argparse
import json
import curses
import logging
from urllib.request import urlopen
from urllib.parse import quote_plus

from monitor import Colors
from monitor import Timer
from monitor import KeyHandlingManager
from monitor import WarningWindow
from monitor import MainWindow
from monitor import Rule
from monitor import DictionaryChecker
from monitor import HeroStatusExtractor
from monitor import ApplicationStatusExtractor


class Monitor:
    def __init__(self, args):
        self.key_manager = KeyHandlingManager()
        self.init_windows()
        self.godname = args.god_name
        self.dump_file = args.dump
        self.state = {}

        curses.noecho()
        curses.cbreak()

        self.init_colors()
        self.init_keys()
        self.init_status_checkers()

    def __del__(self):
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def init_keys(self):
        self.key_manager.register_handler('q', self.quit)
        self.key_manager.register_handler(' ', self.remove_warning)

    def init_windows(self):
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        curses.start_color()

        self.main_window = MainWindow(self.stdscr)
        self.warning_windows = []

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

        curses.init_pair(Colors.ATTENTION,
                         curses.COLOR_WHITE,
                         curses.COLOR_RED)

    def init_status_checkers(self):
        self.info_extractors = []
        self.info_extractors.append(ApplicationStatusExtractor())
        self.info_extractors.append(HeroStatusExtractor())

    def read_state(self):
        logging.debug('%s: reading state',
                      self.read_state.__name__)

        state = None

        try:
            if self.dump_file != None:
                state = self.read_dump(self.dump_file).decode('utf-8')
            else:
                state = self.read_form_url('http://godville.net/gods/api/{0}.json'
                                           .format(quote_plus(self.godname)))
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
            with open(dumpfile, 'rb') as f:
                state = f.read()
        except IOError:
            logging.error('%s: Error reading file %s',
                          self.read_dump.__name__,
                          dumpfile)

        return state

    def handle_key(self):
        try:
            key = self.stdscr.getkey()
            self.key_manager.handle_key(key)
        except curses.error as e:
            if not 'no input' in e.args:
                raise

    def quit(self):
        sys.exit(0)

    def remove_warning(self):
        if len(self.warning_windows) != 0:
            del self.warning_windows[-1]

        self.main_window.update(self.state)

    def check_status(self, state):
        warnings = []

        for extractor in self.info_extractors:
            extractor.extract_info(state)
            extractor.inspect_info()
            self.state[extractor.name] = extractor.info
            warnings += extractor.messages

        for warning in warnings:
            self.warning_windows.append(WarningWindow(self.stdscr, warning))

    def main_loop(self):
        timer = Timer(60)
        self.state = json.loads(self.read_state())
        self.check_status(self.state)
        self.main_window.update(self.state)

        while(True):
            if timer.expired():
                self.state = json.loads(self.read_state())
                self.check_status(self.state)
                self.main_window.update(self.state)
                timer.reset()

            if len(self.warning_windows) != 0:
                self.warning_windows[-1].update({})

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

    parser.add_argument('-D',
                        '--debug',
                        action = 'store_true',
                        help = 'enable debug logs')

    args = parser.parse_args()

    # Configuring logs
    log_level = logging.WARNING

    if (args.debug):
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        filename='pygod.log',
                        filemode='w+',
                        level=log_level)
    logging.debug('Starting PyGod with username %s', args.god_name)

    monitor = Monitor(args)
    monitor.main_loop()


if __name__ == '__main__':
    main()

