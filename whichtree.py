'''Creates the correct variant of a Lifetree given the rulestring.'''
#This file serves as the main access point for __init__.py.
import os
import sys
rootdir = os.path.dirname(__file__)
#Import the genus-determining code.
try:
    from .genera.findgenera import getgenera, RuleHandler
except ImportError:
    sys.path.append(rootdir+'/genera')
    from findgenera import getgenera, RuleHandler
rh = RuleHandler()
#Import the Lifetree code.
sys.path.append(rootdir +'/lifetrees')
sys.path.append(rootdir +'/cythlib')
sys.path.append(rootdir +'/cplusplus')
sys.path.append(rootdir + '/genera')
try:
    from .lifetrees.lifetree import Lifetree as isoLifetree
except ImportError:
    from lifetree import Lifetree as isoLifetree
#Import the Cython code.
try:
    from .cythlib.cylifetree import Lifetree as cyLifetree
    USE_CYTHON = True
except ImportError:
    try:
        from cylifetree import Lifetree as cyLifetree
        USE_CYTHON = True
    except ImportError:
        USE_CYTHON = False
#Import the ruletable code.
try:
    from .lifetrees.tabletree import Lifetree as tableLifetree
except ImportError:
    from tabletree import Lifetree as tableLifetree
#Import the ruletable generation code.
try:
    from .genera.makehistory import makehistory
except ImportError:
    from makehistory import makehistory
#Import the Generations code.
try:
    from .lifetrees.generationstree import Lifetree as genLifetree
except ImportError:
    from generationstree import Lifetree as genLifetree
#Import the C++ lifetree code.
try:
    from .cplusplus.cpplifetree import Lifetree as cppLifetree
except ImportError:
    from cpplifetree import Lifetree as cppLifetree
def lifetree(rule='b3s23'):
    '''Creates a new Lifetree for the given rule.'''
    #This is a wrapper function to take a rule and return the correct Lifetree variant.
    genera = getgenera(rule)
    if genera in ['lifelike', 'isotropic', 'b3s23life']:
        if USE_CYTHON:
            lt = cyLifetree(rule)
        else:
            lt = isoLifetree(rule)
    elif genera == 'eightbit':
        lt = tableLifetree(rule)
    elif genera == 'generations':
        lt = genLifetree(rule)
    elif genera == 'history':
        if rule.lower() == 'lifehistory':
            rule = 'b3s23history'
        with open(rootdir + '/genera/ruletable.rule', 'w', encoding='utf-8') as f:
            f.write(makehistory(rule[:-7]))
        lt = tableLifetree('ruletable.rule')
        os.remove(rootdir + '/genera/ruletable.rule')
    else:
        return None
    lt.genera = genera
    return lt
def cpplifetree(rule='b3s23', force_compile = False):
    '''Creates a new Lifetree using C++ for maximum speed.
Only works with outer-totalistic rules.
Requires MinGW on Windows and g++ on POSIX systems.'''
    if getgenera(rule) not in ['lifelike', 'b3s23life']:
        raise ValueError('Rule '+rule+' is in genus '+getgenera(rule)+' which is not supported.')
    rule = rh.canoniserule(rule)
    if force_compile:
        if os.path.exists(rootdir + '/cplusplus/bin'):
            files = os.listdir(rootdir + '/cplusplus/bin')
        else:
            files = []
        for x in files:
            if x in [rule, rule + '.exe']:
                os.remove(rootdir + '/cplusplus/bin/' + x)
    lt = cppLifetree(rule)
    lt.genera = getgenera(rule)
    return lt
