import os
import sys
import unittest
sys.path.append(os.getcwd())
from monitor import KeyHandlingManager
from monitor import HandlerAlreadyRegisteredException
from monitor import HandlerNotRegisteredException

class KeyHandlingManagerTestFixture(unittest.TestCase):
    def __init__(self, name):
        super(KeyHandlingManagerTestFixture, self).__init__(name)
        self.manager = KeyHandlingManager()

    def key_function1(self):
        return 1

    def key_function2(self):
        return 2

    def key_function3(self):
        return 3


class HandlerRegisteringTest(KeyHandlingManagerTestFixture):
    def positive_test(self):
        self.manager.register_handler('q', self.key_function1)
        self.manager.register_handler('a', self.key_function2)
        self.manager.register_handler('c', self.key_function3)

        self.assertEqual(1, self.manager.handle_key('q'))
        self.assertEqual(2, self.manager.handle_key('a'))
        self.assertEqual(3, self.manager.handle_key('c'))

    def negative_test_already_registered(self):
        try:
            self.manager.register_handler('q', self.key_function1)
            self.manager.register_handler('q', self.key_function2)
            self._assert(False, 'Handler registration exception wasn\'t raised')
        except HandlerAlreadyRegisteredException:
            pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(HandlerRegisteringTest('positive_test'))
    suite.addTest(HandlerRegisteringTest('negative_test_already_registered'))
    return suite


def run_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    run_all()
