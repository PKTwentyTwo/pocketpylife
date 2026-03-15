'''Responsible for determining the genera of a given rule.'''
import re
import os
try:
    from .hensel import RuleHandler
except:
    from hensel import RuleHandler
rh = RuleHandler()
def getgenera(rulestring):
    '''Determines the genera of a rulestring.'''
    if rh.isvalid(rulestring):
        #Valid use of Hensel notation.
        rulestring = rh.canoniserule(rulestring)
        if re.match('b[1-8]*s[0-8]', rulestring):
            return 'lifelike'
        return 'isotropic'
    else:
        if os.path.isfile(rulestring) or os.path.isfile(os.path.dirname(__file__) + '/' + rulestring):
            return 'eightbit'
    raise ValueError('Rule '+rulestring+' is not of a supported type.')

