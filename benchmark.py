import os
os.chdir(os.path.dirname(__file__) + '/..')
print(os.getcwd())
import sys
sys.path.append(os.getcwd())
import pocketpylife
import time
lt = pocketpylife.lifetree('b3s23')
starttime = time.time()
lidka = lt.pattern('''x = 9, y = 15, rule = B3/S23
bo$obo$bo8$8bo$6bobo$5b2obo2$4b3o!''')
lidka = lidka[29055]
print('Final population: '+str(lidka.population))
print('Time taken: '+str(time.time() - starttime))

