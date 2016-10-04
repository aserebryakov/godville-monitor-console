#!/usr/bin/python3

import sys, os
import time
import argparse
import json
import curses
import logging
import configparser
import subprocess
from urllib.request import urlopen
from urllib.parse import quote_plus

from monitor import Colors
from monitor import WarningWindow
from monitor import MainWindow
from monitor import Rule

def unquote_string(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    # Apparently 'unicode_escape' returns string with corrupted utf-8 encoding.
    return bytes(string, "utf-8").decode('unicode_escape').encode("latin1").decode("utf-8")

class Monitor:
    def __init__(self, args):
        self.controls = {}
        self.init_windows()
        self.godname = args.god_name
        self.dump_file = args.state
        self.state = {}
        self.notification_command = args.notification_command
        self.quiet = args.quiet
        self.browser = args.browser if args.browser else "x-www-browser"
        self.refresh_command = args.refresh_command
        self.autorefresh = args.autorefresh
        self.open_browser_on_start = args.open_browser_on_start
        self.rules = []

        curses.noecho()
        try:
            curses.cbreak()
        except curses.error:
            logging.error('curses error: cbreak returned ERR, probably invalid terminal. Try screen or tmux.')
            pass

        self.init_colors()
        self.init_keys()
        self.init_status_checkers()

    def finalize(self):
        curses.echo()
        try:
            curses.nocbreak()
        except curses.error:
            logging.error('curses error: cbreak returned ERR, probably invalid terminal. Try screen or tmux.')
            pass
        curses.endwin()

    def init_keys(self):
        self.controls['q'] = self.quit
        self.controls['f'] = self.open_browser
        self.controls['F'] = self.refresh_session
        self.controls[' '] = self.remove_warning

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
        curses.init_pair(Colors.MONEY,
                         curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)
        curses.init_pair(Colors.HEALING,
                         curses.COLOR_GREEN,
                         curses.COLOR_BLACK)

    def post_warning(self, warning_message):
        if self.quiet:
            return
        if self.notification_command:
            os.system(self.notification_command.format(warning_message)) # FIXME: Highly insecure!
        self.warning_windows.append(WarningWindow(self.stdscr, warning_message))

    def remove_warning(self):
        if len(self.warning_windows) != 0:
            del self.warning_windows[-1]

        self.main_window.update(self.state)

    def handle_expired_session(self):
        if self.autorefresh:
            if self.expired_on_start:
                self.expired_on_start = False
                if self.open_browser_on_start:
                    self.open_browser()
                else:
                    self.refresh_session()
            else:
                self.refresh_session()
        else:
            self.post_warning('Session is expired. Please reconnect.')

    def init_status_checkers(self):
        self.rules.append(Rule(
            lambda info: 'expired' in info and info['expired'],
            self.handle_expired_session
            ))
        self.rules.append(Rule(
            lambda info: 'health' in info and info['health'] > 0 and info['health'] < 40,
            lambda: self.post_warning('Low Health')
            ))
        self.rules.append(Rule(
            lambda info: 'health' in info and info['health'] == 0,
            lambda: self.post_warning('Hero died')
            ))
        self.rules.append(Rule(
            lambda info: info['temple_completed_at'] and (info['health'] > 0.66 * info['max_health']) and info['godpower'] == 100,
            lambda: self.post_warning('Ready for dungeon')
            ))
        self.rules.append(Rule(
            lambda info: 'arena_fight' in info and info['arena_fight'] and info['fight_type'] != 'dungeon',
            lambda: self.post_warning('Hero is in fight')
            ))
        self.rules.append(Rule(
            lambda info: 'arena_fight' in info and info['arena_fight'] and info['fight_type'] == 'dungeon',
            lambda: self.post_warning('Hero descended into dungeon!')
            ))
        self.rules.append(Rule(
            lambda info: sum([(1 if 'activate_by_user' in item else 0) for item in info['inventory'].values()]) > 0,
            lambda: self.post_warning('Hero got an item that can be activated')
            ))

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
            if key in self.controls:
                self.controls[key]()
        except curses.error as e:
            if not 'no input' in e.args:
                raise

    def quit(self):
        sys.exit(0)

    def open_browser(self):
        subprocess.Popen("{0} http://godville.net/superhero".format(self.browser), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # FIXME also unsafe!

    def refresh_session(self):
        if self.refresh_command:
            subprocess.Popen(self.refresh_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # FIXME also unsafe!

    def check_status(self, state):
        for rule in self.rules:
            rule.check(state)

    def main_loop(self):
        UPDATE_INTERVAL = 61
        last_update_time = time.time()

        self.state = json.loads(self.read_state())
        self.expired_on_start = 'expired' in self.state and self.state['expired']
        self.check_status(self.state)
        self.main_window.update(self.state)

        while(True):
            if last_update_time + UPDATE_INTERVAL < time.time():
                last_update_time = time.time()
                self.state = json.loads(self.read_state())
                self.check_status(self.state)
                self.main_window.update(self.state)

            if len(self.warning_windows) != 0:
                self.warning_windows[-1].update({})

            self.handle_key()
            time.sleep(0.1)


def get_config_file(*args):
    xdg_config_dir = os.environ.get('XDG_CONFIG_HOME')
    if not xdg_config_dir:
        xdg_config_dir = os.path.join(os.path.expanduser("~"), ".config")
    app_config_dir = os.path.join(xdg_config_dir, "pygod")
    os.makedirs(app_config_dir, exist_ok=True)
    return os.path.join(app_config_dir, "pygod.ini")

def get_data_dir(*args):
    xdg_data_dir = os.environ.get('XDG_DATA_HOME')
    if not xdg_data_dir:
        xdg_data_dir = os.path.join(os.path.expanduser("~"), ".local", "share")
    app_data_dir = os.path.join(xdg_data_dir, "pygod")
    os.makedirs(app_data_dir, exist_ok=True)
    return app_data_dir

def get_log_dir():
    data_dir = os.environ.get('XDG_LOG_HOME')
    if not data_dir:
        data_dir = os.path.join(os.path.expanduser("~"), ".local", "log")
    logdir = os.path.join(data_dir, "pygod")
    os.makedirs(logdir, exist_ok=True)
    return logdir

def main():
    # Parsing arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('god_name', nargs='?',
                        help = 'Name of the god to me monitored. Overrides value from config file.')

    parser.add_argument('-c',
                        '--config',
                        type = str,
                        help = 'loads config file (default location is XDG_CONFIG_HOME/pygod/pygod.ini')

    parser.add_argument('-s',
                        '--state',
                        type = str,
                        help = 'read state from the dump file (debug option)')

    parser.add_argument('-o',
                        '--open-browser',
                        action='store_true', dest='open_browser_on_start',
                        help = 'opens browser link on start instead of refresh command if session is expired')

    parser.add_argument('-d',
                        '--dump',
                        action = 'store_true',
                        help = 'dump state to file and exit (debug option)')
    parser.add_argument('-q',
                        '--quiet',
                        action = 'store_true',
                        default=False,
                        help = 'do not show notifications')

    parser.add_argument('-D',
                        '--debug',
                        action = 'store_true',
                        help = 'enable debug logs')

    args = parser.parse_args()

    # Config.
    config_files = [get_config_file(), os.path.join(get_data_dir(), "auth.cfg")]
    if args.config:
        config_files.append(args.config)
    settings = configparser.SafeConfigParser()
    settings.read(config_files)
    if args.god_name is None:
        if 'auth' in settings and 'god_name' in settings['auth']:
            args.god_name = unquote_string(settings.get('auth', 'god_name'))
        elif 'main' in settings and 'god_name' in settings['main']:
            args.god_name = unquote_string(settings.get('main', 'god_name'))
    args.notification_command = None
    if 'main' in settings and 'notification_command' in settings['main']:
        args.notification_command = unquote_string(settings.get('main', 'notification_command'))
    args.browser = None
    if 'main' in settings and 'browser' in settings['main']:
        args.browser = unquote_string(settings.get('main', 'browser'))
    args.autorefresh = False
    if 'main' in settings and 'autorefresh' in settings['main']:
        args.autorefresh = unquote_string(settings.get('main', 'autorefresh')).lower() == "true"
    args.refresh_command = None
    if 'main' in settings and 'refresh_command' in settings['main']:
        args.refresh_command = unquote_string(settings.get('main', 'refresh_command'))

    # Configuring logs
    log_level = logging.WARNING

    if (args.debug):
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        filename=os.path.join(get_log_dir(), 'pygod.log'),
                        filemode='a+',
                        level=log_level)

    if args.god_name is None:
        print('God name must be specified either via command line or using config file!')
        sys.exit(1)

    logging.debug('Starting PyGod with username %s', args.god_name)

    if args.dump:
        state = None
        if args.state:
            with open(args.state, 'rb') as f:
                state = f.read().decode('utf-8')
        else:
            url = 'http://godville.net/gods/api/{0}.json'.format(quote_plus(args.god_name))
            connection = urlopen(url)
            state = connection.read().decode('utf-8')
        prettified_state = json.dumps(json.loads(state), indent=4, ensure_ascii=False)
        dump_file = '{0}.json'.format(args.god_name)
        with open(dump_file, 'wb') as f:
            f.write(prettified_state.encode('utf-8'))
        print('Dumped current state to {0}.'.format(dump_file))
    else:
        try:
            monitor = Monitor(args)
            monitor.main_loop()
        finally:
            monitor.finalize()


if __name__ == '__main__':
    main()

