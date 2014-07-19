import os
import sys
import time
import unittest
sys.path.append(os.getcwd())
from monitor import Timer

class TimerTest(unittest.TestCase):
    def timer_test(self):
        interval = 10
        timer = Timer(interval)
        for i in range(0, 10):
            time.sleep(interval/2)
            print('Checking')
            if timer.expired():
                print('Expired')
                timer.reset()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TimerTest('timer_test'))
    return suite

def run_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    run_all()
