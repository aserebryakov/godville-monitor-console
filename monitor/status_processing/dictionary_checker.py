import logging
from .rule import Rule

class DictionaryChecker:
    '''
    Class that implements checking of a given dictionary
    in accordance to list of rules
    '''

    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        '''
        Adds rule to a rule list
        '''

        logging.debug('%s: New rule is added : %s',
                      self.add_rule.__name__,
                      rule.to_string())

        self.rules.append(rule)

    def check_rules(self, dictionary):
        '''
        Checks the dictionary for all rules in list
        '''

        messages = []

        for rule in self.rules:
            if rule.key in dictionary.keys():
                if rule.check(dictionary[rule.key]) == True:
                    messages.append(rule.messages)
            else:
                logging.debug('%s: Key not found : %s',
                              self.check_rules.__name__,
                              rule.key)
