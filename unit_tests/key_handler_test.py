import os
import sys
import unittest
sys.path.append(os.getcwd())
from core import KeyHandlingManager

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
        self.manager.register_handler(1, self.key_function1)
        self.manager.register_handler(2, self.key_function2)
        self.manager.register_handler(3, self.key_function3)

        self.assertEqual(1, self.manager.handle_keys([1]))
        self.assertEqual(2, self.manager.handle_keys([2]))
        self.assertEqual(3, self.manager.handle_keys([3]))

    def negative_test_already_registered(self):
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
