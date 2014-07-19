import os
import sys
import unittest
sys.path.append(os.getcwd())
from monitor import Rule

class RuleTest(unittest.TestCase):
    def rule_check_positive(self):
        rule = Rule('example', '==', False, 'Message')
        self.assertEqual(True, rule.check(False))
        self.assertEqual(False, rule.check(False))
        self.assertEqual(False, rule.check(True))
        self.assertEqual(True, rule.check(False))

    def rule_check_negative_incorrect_value(self):
        rule = Rule('example', '==', False, 'Message')
        self.assertEqual(False, rule.check('assert(False)'))

    def rule_check_negative_incorrect_ethalon(self):
        rule = Rule('example', '==', 'assert(False)', 'Message')
        self.assertEqual(False, rule.check(False))

    def rule_check_negative_incorrect_condition(self):
        rule = Rule('example', '== 0 or True: assert(False) #', False, 'Message')
        self.assertEqual(False, rule.check(False))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(RuleTest('rule_check_positive'))
    suite.addTest(RuleTest('rule_check_negative_incorrect_value'))
    suite.addTest(RuleTest('rule_check_negative_incorrect_ethalon'))
    suite.addTest(RuleTest('rule_check_negative_incorrect_condition'))
    return suite

def run_all():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    run_all()
