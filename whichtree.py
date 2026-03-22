'''Creates the correct variant of a Lifetree given the rulestring.'''
import os
import sys
#Import the genus-determining code.
try:
    from .genera.findgenera import getgenera
except ImportError:
    sys.path.append(os.path.dirname(__file__)+'/genera')
    from findgenera import getgenera
#Import the Lifetree code.
try:
    from .lifetree import Lifetree as isoLifetree
except ImportError:
    from lifetree import Lifetree as isoLifetree
#Import the Cython code.
try:
    from .cylifetree import Lifetree as cyLifetree
    USE_CYTHON = True
except ImportError:
    try:
        from cylifetree import Lifetree as cyLifetree
        USE_CYTHON = True
    except ImportError:
        USE_CYTHON = False
#Import the ruletable code.
try:
    from .tabletree import Lifetree as tableLifetree
except ImportError:
    from tabletree import Lifetree as tableLifetree
#Import the Generations code.
try:
    from .generationstree import Lifetree as genLifetree
except ImportError:
    from generationstree import Lifetree as genLifetree
def lifetree(rule='b3s23'):
    '''Creates a new Lifetree for the given rule.'''
    #This is a wrapper function to take a rule and return the correct Lifetree variant.
    genera = getgenera(rule)
    if genera in ['lifelike', 'isotropic', 'b3s23life']:
        if USE_CYTHON:
            return cyLifetree(rule)
        return isoLifetree(rule)
    if genera == 'eightbit':
        return tableLifetree(rule)
    if genera == 'generations':
        return genLifetree(rule)
    return 'unknown'
