'''A Python package for manipulation of patterns in cellular automata. '''
import os
#Import the routing functions for Lifetrees:
from .whichtree import lifetree, cpplifetree
#Import the compiler regardless:
try:
    from .cythlib.cython_setup import cython_compile, remove_cython_compilation
    __all__ = ['lifetree', 'cpplifetree', 'cython_compile', 'remove_cython_compilation']
except ImportError:
    __all__ = ['lifetree', 'cpplifetree']
#Import MinGW related functions on Windows:
if os.name == 'nt':
    from .cplusplus.mingw import install_mingw
    __all__ += ['install_mingw']
__all__.sort()
__version__ = '1.4.0'
