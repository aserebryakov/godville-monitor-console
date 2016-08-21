import curses
from ..core import MonitorWindowBase
from ..core import TextEntry
from ..core import Colors

class MainWindow(MonitorWindowBase):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__('', height, width, stdscr)

        self._subwindows = []

        statusWindow = MonitorWindowBase('Status', 10, 22, self.window, 0, 0)
        statusWindow.add_text_entry('', 'name')
        statusWindow.add_text_entry('HP', 'health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Max HP', 'max_health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Power, %', 'godpower', color=Colors.POWER_POINTS)
        statusWindow.add_text_entry('EXP, %', 'exp_progress')
        statusWindow.add_text_entry('Town', 'town_name')
        statusWindow.add_text_entry('Distance', 'distance')
        self._subwindows.append(statusWindow)

        questWindow = MonitorWindowBase('Quest', 8, width - 22, self.window, 0, 22)
        questWindow.add_text_entry('', 'quest')
        questWindow.add_text_entry('Progress, %', 'quest_progress')
        questWindow.add_text_entry('', '')
        questWindow.add_text_entry('', 'diary_last')
        self._subwindows.append(questWindow)

        petWindow = MonitorWindowBase('Pet', 6, 22, self.window, 10, 0)
        petWindow.add_text_entry('', lambda state: state['pet']['pet_class'])
        petWindow.add_text_entry('', lambda state: state['pet']['pet_name'])
        petWindow.add_text_entry('Level', lambda state: state['pet']['pet_level'])
        self._subwindows.append(petWindow)

        inventoryWindow = MonitorWindowBase('Inventory', 8, width - 22, self.window, 8, 22)
        inventoryWindow.add_text_entry('Gold', 'gold_approx')
        inventoryWindow.add_text_entry('Bricks', 'bricks_cnt')
        inventoryWindow.add_text_entry('Wood', 'wood_cnt')
        inventoryWindow.add_text_entry('Useful Items',
            lambda state: sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('High Cost Items',
            lambda state: sum([(1 if item['price'] > 0 else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('Total Items', 'inventory_num')
        self._subwindows.append(inventoryWindow)

        applicationStatusWindow = MonitorWindowBase('Application Status', height - 16, width, self.window, 16, 0)
        applicationStatusWindow.add_text_entry('',
            lambda state: 'Session is expired' if 'expired' in state else 'Session is active')
        self._subwindows.append(applicationStatusWindow)

    def update(self, state):
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()

