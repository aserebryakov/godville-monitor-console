import curses
from ..core import TiledWindow
from ..core import TextEntry
from ..core import Colors

from .status_window import StatusWindow
from .quest_window import QuestWindow
from .pet_window import PetWindow
from .inventory_window import InventoryWindow
from .application_status_window import ApplicationStatusWindow


class MainWindow(TiledWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__('', height, width, stdscr)

        self._subwindows = []

        statusWindow    = StatusWindow(self.window)
        statusWindow.add_text_entry('', 'name')
        statusWindow.add_text_entry('HP', 'health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Max HP', 'max_health', color=Colors.HEALTH_POINTS)
        statusWindow.add_text_entry('Power, %', 'godpower', color=Colors.POWER_POINTS)
        statusWindow.add_text_entry('EXP, %', 'exp_progress')

        statusWindow.add_text_entry('Town', 'town_name')
        statusWindow.add_text_entry('Distance', 'distance')
        questWindow     = QuestWindow(self.window, None, statusWindow)
        questWindow.add_text_entry('', 'quest')
        questWindow.add_text_entry('Progress, %', 'quest_progress')
        questWindow.add_text_entry('', '')
        questWindow.add_text_entry('', 'diary_last')
        petWindow       = PetWindow(self.window, statusWindow, None)
        petWindow.add_text_entry('', lambda state: state['pet']['pet_class'])
        petWindow.add_text_entry('', lambda state: state['pet']['pet_name'])
        petWindow.add_text_entry('Level', lambda state: state['pet']['pet_level'])
        inventoryWindow = InventoryWindow(self.window,
                                          questWindow,
                                          statusWindow)
        inventoryWindow.add_text_entry('Gold', 'gold_approx')
        inventoryWindow.add_text_entry('Bricks', 'bricks_cnt')
        inventoryWindow.add_text_entry('Wood', 'wood_cnt')
        inventoryWindow.add_text_entry('Useful Items',
            lambda state: sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('High Cost Items',
            lambda state: sum([(1 if item['price'] > 0 else 0) for item in state['inventory'].values()]))
        inventoryWindow.add_text_entry('Total Items', 'inventory_num')

        applicationStatusWindow = ApplicationStatusWindow(self.window,
                                                          petWindow,
                                                          None)
        applicationStatusWindow.add_text_entry('',
            lambda state: 'Session is expired' if 'expired' in state else 'Session is active')

        self._subwindows.append(statusWindow)
        self._subwindows.append(questWindow)
        self._subwindows.append(petWindow)
        self._subwindows.append(inventoryWindow)
        self._subwindows.append(applicationStatusWindow)

    def update(self, state):
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()

