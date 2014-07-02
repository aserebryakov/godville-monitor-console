import unittest
from key_handler import KeyHandlingManager

class KeyHandlingManagerTestFixture(unittest.TestCase):
    self.manager = KeyHandlingManager()

    def key_function1(self):
        return 1

    def key_function2(self):
        return 2

    def key_function3(self):
        return 3

class HandlerRegisteringTest(KeyHandlingManager):
    def runTest(self):
        self.manager.register_handler(1, self.key_function1)
        self.manager.register_handler(2, self.key_function2)
        self.manager.register_handler(3, self.key_function3)
        self.assertEqual(1, self.handle_keys([1])
        self.assertEqual(2, self.handle_keys([2])
        self.assertEqual(3, self.handle_keys([3])

class HandlerRegisteringErrorTest(KeyHandlingManager):
    def runTest(self):
        pass
