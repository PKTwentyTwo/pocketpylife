'''Responsible for dealing with C++ compilation.'''
import os
import platform
import sys
try:
    from ..hensel import RuleHandler
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/genera')
    from hensel import RuleHandler
