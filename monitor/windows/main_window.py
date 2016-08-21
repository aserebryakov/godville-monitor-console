import curses
from ..core import MonitorWindowBase
from ..core import TextEntry
from ..core import Colors

def inventory_list(state):
    item_list = []
    for item_name in state['inventory']:
        item_state = state['inventory'][item_name]
        item_state['name'] = item_name
        item_list.append(item_state)
    item_list.sort(key=lambda item: item['pos'])
    for item in item_list:
        yield '- {0}'.format(item['name']), None

class MainWindow(MonitorWindowBase):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__(stdscr, '')

        self._subwindows = []

        # Column 1: Main hero stats.
        wnd = MonitorWindowBase(self.window, 'Session', 0, 0, 22, 3)
        wnd.add_text_entry('', lambda state: 'Expired' if 'expired' in state else 'Active')
        self._subwindows.append(wnd)

        wnd = MonitorWindowBase(self.window, 'God', 0, 3, 22, 4)
        wnd.add_text_entry('', 'godname')
        wnd.add_text_entry('Power:', 'godpower', color=Colors.POWER_POINTS)
        self._subwindows.append(wnd)

        wnd = MonitorWindowBase(self.window, 'Hero', 0, 7, 22, 12)
        wnd.add_text_entry('', 'name')
        wnd.add_text_entry('', 'alignment')
        wnd.add_text_entry('HP:', lambda state: '{0}/{1}'.format(state['health'], state['max_health']), color=Colors.HEALTH_POINTS)
        wnd.add_text_entry('Lvl:', lambda state: '{0} ({1}%)'.format(state['level'], state['exp_progress']))
        wnd.add_text_entry('Clan:', lambda state: '{0}, {1}'.format(state['clan'], state['clan_position']))
        wnd.add_text_entry('Temple:', lambda state: 'done' if state['temple_completed_at'] else str(state['bricks_cnt']))
        wnd.add_text_entry('Ark:', lambda state: 'done' if state['ark_completed_at'] else str(state['wood_cnt']))
        wnd.add_text_entry('Location:', lambda state: 'Fight!' if state['arena_fight'] else ( state['town_name'] if state['town_name'] else '{0} pl'.format(state['distance']) ) )
        self._subwindows.append(wnd)

        wnd = MonitorWindowBase(self.window, 'Pet', 0, 19, 22, 5)
        wnd.add_text_entry('', lambda state: '{0} {1}'.format(state['pet']['pet_class'], state['pet']['pet_name']))
        wnd.add_text_entry('Level:', lambda state: state['pet']['pet_level'])
        self._subwindows.append(wnd)

        if height > 24:
            wnd = MonitorWindowBase(self.window, '', 0, 24, 22, None)
            self._subwindows.append(wnd)

        # Column 2: Inventory.
        wnd = MonitorWindowBase(self.window, 'Inventory', 22, 0, 30, None)
        wnd.add_text_entry('Gold:', 'gold_approx')
        wnd.add_text_entry('Items:', lambda state: '{0}/{1}'.format(state['inventory_num'], state['inventory_max_num']))
        wnd.add_text_entry('Useful Items',
            lambda state: sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()]))
        wnd.add_text_entry('High Cost Items',
            lambda state: sum([(1 if item['price'] > 0 else 0) for item in state['inventory'].values()]))
        wnd.add_list_entry(inventory_list)
        self._subwindows.append(wnd)

        # Column 3: Quest, diary etc.
        wnd = MonitorWindowBase(self.window, 'Log', 52, 0, None, None)
        wnd.add_text_entry('Quest: ', lambda state: '{0} ({1}%)'.format(state['quest'], state['quest_progress']))
        wnd.add_text_entry('', '')
        wnd.add_text_entry('', lambda state: '"{0}"'.format(state['motto']))
        wnd.add_text_entry('', lambda x: '* * *')
        wnd.add_text_entry('- ', 'diary_last')
        self._subwindows.append(wnd)

    def update(self, state):
        super(MainWindow, self).update(state)
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()

