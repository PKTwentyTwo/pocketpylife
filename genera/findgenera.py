'''Responsible for determining the genera of a given rule.'''
import re
import os
try:
    from .hensel import RuleHandler
except ImportError:
    from hensel import RuleHandler
try:
    from .generations import splitgenrule
except ImportError:
    from generations import splitgenrule
rh = RuleHandler()
def getgenera(rulestring):
    '''Determines the genera of a rulestring.'''
    try:
        splitgenrule(rulestring)
        return 'generations'
    except ValueError:
        pass
    if rh.isvalid(rulestring):
        #Valid use of Hensel notation.
        rulestring = rh.canoniserule(rulestring)
        if rulestring == 'b3s23':
            return 'b3s23life'
        rulestring += '\n'
        if re.match('b[1-8]*s[0-8]*\n', rulestring):
            return 'lifelike'
        return 'isotropic'
    if os.path.isfile(rulestring) or os.path.isfile(os.path.dirname(__file__) + '/' + rulestring):
        return 'eightbit'
    raise ValueError('Rule '+rulestring+' is not of a supported type.')
