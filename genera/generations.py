'''Parses Generations rules.'''
import re
try:
    from .hensel import RuleHandler
except ImportError:
    from hensel import RuleHandler
rh = RuleHandler()
def splitgenrule(rule):
    '''Splits a rule into its components, and raises an error if there are formatting issues.'''
    birth = ''
    survival = ''
    gen = ''
    splitrule = rule.split('/')
    if len(splitrule) != 3:
        raise ValueError('A Generations rule requires three sections in the rulestring.')
    count = 0
    for x in splitrule:
        count += 1
        if x.startswith('b') or x.startswith('B'):
            #Birth conditions.
            birth += x.lower().replace('b', '')
        elif x.startswith('s') or x.startswith('S'):
            #Survival conditions.
            survival += x.lower().replace('s', '')
        else:
            #Just do the standard order of survival/birth/gens:
            if count == 1:
                survival += x.lower()
            elif count == 2:
                birth += x.lower()
            else:
                gen += x.lower()
    #Validity checks:
    testrule = 'b' + birth + 's' + survival
    if not rh.isvalid(testrule):
        raise ValueError('Illegal birth or survival condition in rulestring.')
    if not gen.isnumeric():
        raise ValueError('The total number of states must be numeric.')
    if int(gen) > 26 or int(gen) < 3:
        raise ValueError('The number of states given must be between 3 and 26.')
    return (birth, survival, gen)
def canonisegenstringinternal(rulestring):
    '''Canonises a Generations rulestring for internal use.'''
    birth, survival, gen = splitgenrule(rulestring)
    filteredstring = rh.canoniserule('b' + birth + 's' + survival)
    newrulestring = 'g' + gen + filteredstring
    return newrulestring
def canonisegenstringexternal(rulestring):
    '''Canonises a Generations rulestring for external display.'''
    birth, survival, gen = splitgenrule(rulestring)
    filteredstring = rh.canoniserule('b' + birth + 's' + survival)
    newrulestring = 's' + filteredstring[filteredstring.find('s')+1:] + '/b' + filteredstring[1:filteredstring.find('s')] + '/' + gen
    return newrulestring
def getgenset(rulestring):
    '''Returns the set used for processing by Generations Lifetrees.'''
    rulestring = canonisegenstringinternal(rulestring)
    isorulestring = rulestring[rulestring.find('b'):]
    return rh.makeconditionset(isorulestring)
