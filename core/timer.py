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
        current_time = int(time.perf_counter())
        result = (current_time > self._end_time)

        return result

    def reset(self):
        current_time = int(time.perf_counter())
        self._end_time =  current_time + self.interval
        logging.debug('%s: resetting timer \n start time %d\n end time is %d',
                      self.reset.__name__,
                      current_time,
                      self._end_time)

