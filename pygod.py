#!/usr/bin/python3

import sys, os
import time
import argparse
import json
import curses
import logging
import configparser
import subprocess
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus

from monitor import Colors
from monitor import WarningWindow
from monitor import MainWindow
from monitor import Rule

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

def load_rule_module(module_filename):
    ''' Loading custom rules (see example rules.py for usage).
    Custom rules module is loaded from $XDG_DATA_HOME/pygod/rules.py
    '''
    if not os.path.isfile(module_filename):
        return []
    import types
    module_name = os.path.splitext(os.path.basename(module_filename))[0]
    is_function = lambda var: isinstance(var, types.FunctionType)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_filename)
        custom_rules_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(custom_rules_module)
    except AttributeError:
        from importlib.machinery import SourceFileLoader
        custom_rules_module = SourceFileLoader(module_name, module_filename).load_module()

    public_objects = [name for name in dir(custom_rules_module) if not name.startswith('_')]
    return list(filter(is_function, map(custom_rules_module.__dict__.get, public_objects)))

# Basic custom rules.
CUSTOM_RULE_MODULE = os.path.join(get_data_dir(), "rules.py")
CUSTOM_RULES = load_rule_module(CUSTOM_RULE_MODULE)

def unquote_string(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    # Apparently 'unicode_escape' returns string with corrupted utf-8 encoding.
    return bytes(string, "utf-8").decode('unicode_escape').encode("latin1").decode("utf-8")

def load_hero_state(godname):
    url = 'http://godville.net/gods/api/{0}'.format(quote_plus(args.god_name))
    connection = urlopen(url)
    if connection is None or connection.getcode() == 404:
        old_url = 'http://godville.net/gods/api/{0}.json'.format(quote_plus(args.god_name))
        logging.error(
                'load_hero_state: new api url %s returned 404\n'
                '                 will try old api url %s',
                url, old_url)
        connection = urlopen(old_url)
    return connection.read().decode('utf-8')

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
        self.prev_state = None
        self.error = None

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
        curses.use_default_colors()
        COLOR_TRANSPARENT = -1
        curses.init_pair(Colors.STANDART,
                         curses.COLOR_WHITE,
                         COLOR_TRANSPARENT)

        curses.init_pair(Colors.HEALTH_POINTS,
                         curses.COLOR_RED,
                         COLOR_TRANSPARENT)

        curses.init_pair(Colors.POWER_POINTS,
                         curses.COLOR_BLUE,
                         COLOR_TRANSPARENT)

        curses.init_pair(Colors.ATTENTION,
                         curses.COLOR_WHITE,
                         curses.COLOR_RED)
        curses.init_pair(Colors.MONEY,
                         curses.COLOR_YELLOW,
                         COLOR_TRANSPARENT)
        curses.init_pair(Colors.HEALING,
                         curses.COLOR_GREEN,
                         COLOR_TRANSPARENT)

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
        for custom_rule in CUSTOM_RULES:
            action = custom_rule(None)
            if isinstance(action, str) or isinstance(action, unicode):
                # Trick to bind message text at the creation time, not call time.
                action = lambda action=action: self.post_warning(action)
            self.rules.append(Rule(custom_rule, action))

    def read_state(self):
        logging.debug('%s: reading state',
                      self.read_state.__name__)

        state = None

        try:
            if self.dump_file != None:
                state = self.read_dump(self.dump_file)
            else:
                state = load_hero_state(self.godname)
            self.error = None
        except urllib.error.URLError as e:
            logging.error('%s: reading state error \n %s',
                          self.read_state.__name__,
                          str(e))
            self.post_warning('Connection error: {0}'.format(e))
            if self.prev_state is None:
                print('Error occured, please see the pygod.log')
                sys.exit(1)
            state = self.prev_state
            self.error = str(e)
        except Exception as e:
            logging.error('%s: reading state error \n %s %s %s',
                          self.read_state.__name__,
                          str(type(e)), repr(e), str(e))
            print('Error occured, please see the pygod.log')

            sys.exit(1)
        self.prev_state = state
        return state

    def read_dump(self, dumpfile):
        state = None

        try:
            with open(dumpfile, 'rb') as f:
                state = f.read().decode('utf-8')
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
        if self.error:
            self.state['error'] = self.error
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
            state = load_hero_state(args.god_name)
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

