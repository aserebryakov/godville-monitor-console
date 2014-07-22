import os
import sys
import unittest
sys.path.append(os.getcwd())
from monitor import Rule
from monitor import DictionaryChecker


class DictionaryCheckerTestFixture(unittest.TestCase):
    def setUp(self):
        self.checker = DictionaryChecker()
        self.rules = {'0': 'This is first rule',
                      '1': 'This is the second rule',
                      '2': 'This is the third rule'}

        self.checker.add_rule(Rule('0', '<', 20, self.rules['0']))
        self.checker.add_rule(Rule('1', '==', 20, self.rules['1']))
        self.checker.add_rule(Rule('2', '==', False, self.rules['2']))


class DictionaryCheckerTest(DictionaryCheckerTestFixture):
    def single_rule_test(self):
        dictionary = {'0' : 400,
                      '1' : 20,
                      '2' : True}

        messages = self.checker.check_rules(dictionary)
        self.assertEqual(1, len(messages))
        self.assert_(self.rules['1'] == messages[0])

    def multiple_rule_test(self):
        dictionary = {'0' : 19,
                      '1' : 20,
                      '2' : True}

        messages = self.checker.check_rules(dictionary)
        self.assertEqual(2, len(messages))
        self.assert_(self.rules['0'] == messages[0])
        self.assert_(self.rules['1'] == messages[1])

    def incorrect_type_test(self):
        dictionary = {'0' : 19,
                      '1' : 'asd',
                      '2' : True}

        messages = self.checker.check_rules(dictionary)
        self.assertEqual(1, len(messages))
        self.assert_(self.rules['0'] == messages[0])

    def incorrect_comparison_test(self):
        dictionary = {'0' : 19,
                      '1' : False,
                      '2' : True}

        messages = self.checker.check_rules(dictionary)
        self.assertEqual(1, len(messages))
        self.assert_(self.rules['0'] == messages[0])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DictionaryCheckerTest('single_rule_test'))
    suite.addTest(DictionaryCheckerTest('multiple_rule_test'))
    suite.addTest(DictionaryCheckerTest('incorrect_type_test'))
    suite.addTest(DictionaryCheckerTest('incorrect_comparison_test'))
    return suite

def run_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    run_all()
