import time
import logging

class Timer:
    def __init__(self, interval):
        self._interval = interval
        self._end_time = 0
        self.reset()

    @property
    def interval(self):
        return self._interval

    def expired(self):
        result = (int(time.perf_counter()) > self._end_time)

        logging.debug('%s: result is %s',
                      self.expired.__name__,
                      str(result))

        return result

    def reset(self):
        self._end_time = int(time.perf_counter()) + self.interval
        logging.debug('%s: resetting timer to time %s',
                      self.reset.__name__,
                      str(self._end_time))

