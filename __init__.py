'''A Python package for manipulation of patterns in cellular automata. '''
import os
#Import the routing function for Lifetrees:
from .whichtree import lifetree
#Import the compiler regardless:
try:
    from .cython_setup import cython_compile, remove_cython_compilation
    __all__ = ['lifetree', 'cython_compile', 'remove_cython_compilation']
except ImportError:
    __all__ = ['lifetree']
__version__ = '0.2.0'

