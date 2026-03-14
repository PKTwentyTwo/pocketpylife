print('pocketpylife by PK22')
print('A Python package for manipulation of patterns in cellular automata.')
print('-----------')
try:
    from lifetree import Lifetree
except ImportError:
    from .lifetree import Lifetree
import time
lt = Lifetree('b3s23')
pt = lt.pattern('o$3o$bo!')
starttime = time.time()
pt = pt[1103]
endtime = time.time()
print('Simulated 1103 generations of the R-pentomino in '+str(round(endtime - starttime, 2))+' seconds.')
print('-----------')
print('''       oo   oo
      o  o o  o
      oo o o oo
         o o
      oo o o oo
       o o o o
 oo o  o o o o  o oo
o o ooo  o o  ooo o o
o        o o        o
 oooooooo   oooooooo

 oooooooo   oooooooo
o        o o        o
o o ooo  o o  ooo o o
 oo o  o o o o  o oo
       o o o o
      oo o o oo
         o o
      oo o o oo
      o  o o  o
       oo   oo
''')
