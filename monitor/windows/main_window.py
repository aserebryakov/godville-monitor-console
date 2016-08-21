import curses
from ..core import MonitorWindowBase
from ..core import TextEntry
from ..core import Colors

class MainWindow(MonitorWindowBase):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__(stdscr, '')

        self._subwindows = []

        statusWindow = MonitorWindowBase(self.window, 'Status', 0, 0, 22, 10)
        statusWindow.add_text_entry('', 'name')
        statusWindow.add_text_entry('HP', 'health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Max HP', 'max_health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Power, %', 'godpower', color=Colors.POWER_POINTS)
        statusWindow.add_text_entry('EXP, %', 'exp_progress')
        statusWindow.add_text_entry('Town', 'town_name')
        statusWindow.add_text_entry('Distance', 'distance')
        self._subwindows.append(statusWindow)

        questWindow = MonitorWindowBase(self.window, 'Quest', 22, 0, None, 8)
        questWindow.add_text_entry('', 'quest')
        questWindow.add_text_entry('Progress, %', 'quest_progress')
        questWindow.add_text_entry('', '')
        questWindow.add_text_entry('', 'diary_last')
        self._subwindows.append(questWindow)

        petWindow = MonitorWindowBase(self.window, 'Pet', 0, 10, 22, 6)
        petWindow.add_text_entry('', lambda state: state['pet']['pet_class'])
        petWindow.add_text_entry('', lambda state: state['pet']['pet_name'])
        petWindow.add_text_entry('Level', lambda state: state['pet']['pet_level'])
        self._subwindows.append(petWindow)

        inventoryWindow = MonitorWindowBase(self.window, 'Inventory', 22, 8, None, 8)
        inventoryWindow.add_text_entry('Gold', 'gold_approx')
        inventoryWindow.add_text_entry('Bricks', 'bricks_cnt')
        inventoryWindow.add_text_entry('Wood', 'wood_cnt')
        inventoryWindow.add_text_entry('Useful Items',
            lambda state: sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('High Cost Items',
            lambda state: sum([(1 if item['price'] > 0 else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('Total Items', 'inventory_num')
        self._subwindows.append(inventoryWindow)

        applicationStatusWindow = MonitorWindowBase(self.window, 'Session', 0, 16, 22, 3)
        applicationStatusWindow.add_text_entry('',
            lambda state: 'Expired' if 'expired' in state else 'Active')
        self._subwindows.append(applicationStatusWindow)

    def update(self, state):
        super(MainWindow, self).update(state)
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()

