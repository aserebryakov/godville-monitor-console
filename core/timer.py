import time

class Timer:
    def __init__(self, interval):
        self._interval = interval
        self._end_time = 0
        self.reset()

    @property
    def interval(self):
        return self._interval

    def expired(self):
        return (int(time.perf_counter()) > self._end_time)

    def reset(self):
        self._end_time = int(time.perf_counter()) + self.interval

