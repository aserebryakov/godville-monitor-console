import os
import sys
import unittest
sys.path.append(os.getcwd())
from monitor import Rule
from monitor import DictionaryChecker


class DictionaryCheckerTestFixture(unittest.TestCase):
    def setUp(self):
        self.checker = DictionaryChecker()
        rules = {'0': 'This is first rule',
                 '1': 'This is the second rule',
                 '2': 'This is the third rule'}

        self.checker.add_rule(Rule('0', '<', 20, rules['0']))
        self.checker.add_rule(Rule('1', '==', 20, rules['1']))
        self.checker.add_rule(Rule('2', '==', False, rules['2']))


class DictionaryCheckerTest(DictionaryCheckerTestFixture):
    def single_rule_test(self):
        dictionary = {'1' : 400,
                      '2' : 20,
                      '3' : True}


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DictionaryCheckerTest('single_rule_test'))
    return suite

def run_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    run_all()
