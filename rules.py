# Example module for custom rules.
# Save it to $XDG_DATA_HOME/pygod/rules.py
#
# All callable objects (function, classes, lambdas etc) are loaded when monitor is started.
# Objects that starts with underscore are ignored as module's private.
#
# Rule function should take single argument of Godville hero's state dict and return True or False to indicate that condition is met.
# When state is set to None, it should return function object or a string. It will be executed when condition becomes True for the first time.
# If string is returned, Monitor.post_warning() will be used as action as the string is used as text of the warning.
#
# All exceptions from checks or actions are caught and logged to pygod.log file.

def low_health(state):
    if state is None:
        return 'Low Health'
    return 'health' in state and state['health'] > 0 and state['health'] < 40

def hero_died(state):
    if state is None:
        return 'Hero died'
    return 'health' in state and state['health'] == 0

def ready_for_dungeon(state):
    if state is None:
        return 'Ready for dungeon'
    return state['temple_completed_at'] and (state['health'] > 0.66 * state['max_health']) and state['godpower'] == 100

def boss_fight(state):
    if state is None:
        return 'Hero is in fight'
    return 'arena_fight' in state and state['arena_fight'] and state['fight_type'] != 'dungeon'

def in_dungeon(state):
    if state is None:
        return 'Hero descended into dungeon!'
    return 'arena_fight' in state and state['arena_fight'] and state['fight_type'] == 'dungeon'

def active_item(state):
    if state is None:
        return 'Hero got an item that can be activated'
    return 0 < sum([(1 if 'activate_by_user' in item else 0) for item in state['inventory'].values()])
