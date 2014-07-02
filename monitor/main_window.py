import curses
from core import MonitorWindow
from core import TextEntry
from core import Colors

from .status_window import StatusWindow
from .quest_window import QuestWindow
from .pet_window import PetWindow
from .inventory_window import InventoryWindow
from .application_status_window import ApplicationStatusWindow


class MainWindow(MonitorWindow):
    def __init__(self, stdscr):
        (height, width) = stdscr.getmaxyx()
        super(MainWindow, self).__init__('', stdscr, None, None, height, width)

        self._subwindows = []

        statusWindow    = StatusWindow(self.window, None, None)
        questWindow     = QuestWindow(self.window, None, statusWindow)
        petWindow       = PetWindow(self.window, statusWindow, None)
        inventoryWindow = InventoryWindow(self.window,
                                          questWindow,
                                          statusWindow)

        applicationStatusWindow = ApplicationStatusWindow(self.window,
                                                          petWindow,
                                                          None)

        self._subwindows.append(statusWindow)
        self._subwindows.append(questWindow)
        self._subwindows.append(petWindow)
        self._subwindows.append(inventoryWindow)
        self._subwindows.append(applicationStatusWindow)

    def update(self, state):
        for window in self._subwindows:
            window.update(state)

        self.window.refresh()

