import logging
from .monitor_window import MonitorWindowBase

class TiledWindow(MonitorWindowBase):
    '''
    Base class for all tiled windows
    '''
    def __init__(self,
                 title,
                 height,
                 width,
                 parent_window,
                 top_window = None,
                 left_window = None):

        self.top_window   = top_window
        self.left_window  = left_window

        window_y = 0
        window_x = 0

        if top_window != None:
            window_y           = top_window.y + top_window.height

        if left_window != None:
            window_x           = left_window.x + left_window.width

        super(TiledWindow, self).__init__(title,
                                          height,
                                          width,
                                          parent_window,
                                          window_y,
                                          window_x)
