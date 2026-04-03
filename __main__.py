#!/usr/bin/python3
import os
import sys
import time
print('pocketpylife by PK22')
print('A Python package for manipulation of patterns in cellular automata.')
print('-----------')
try:
    from .whichtree import lifetree
    lt = lifetree('b3s23')
except:
    sys.path = [os.path.dirname(os.path.dirname(__file__))] + sys.path
    import pocketpylife
    lt = pocketpylife.lifetree('b3s23')
pt = lt.pattern('o$3o$bo!')
starttime = time.time()
pt = pt[1103]
endtime = time.time()
print('Simulated 1103 generations of the R-pentomino in '+str(round(endtime - starttime, 2))+' seconds.')
print('-----------')
