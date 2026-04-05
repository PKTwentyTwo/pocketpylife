'''Tests the speed of the C++ lifetree.
Used for identifying which compiler flags are suitable.'''
import os
import sys
import time
compilerargs = sys.argv[1:]
rootdir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(rootdir + '/cplusplus')
sys.path.append(rootdir + '/cythlib')
sys.path.append(rootdir + '/lifetrees')
try:
    from ..cplusplus.cpplifetree import Lifetree as cpplifetree
except ImportError:
    from cpplifetree import Lifetree as cpplifetree
try:
    from ..cplusplus.compilecontrol import compilerule
except ImportError:
    from compilecontrol import compilerule
compilerule('b3s23', compilerargs)
lidka_rle = '''x = 9, y = 15, rule = B3/S23
bo$obo$bo8$8bo$6bobo$5b2obo2$4b3o!'''
def test(lt, name):
    starttime = time.time()
    pt = lt.pattern(lidka_rle)
    evpt = pt[29055]
    print(evpt.population)
    timetaken = time.time() - starttime
    print(name + ' finished testing in '+str(round(timetaken, 3))+' seconds.')
test(cpplifetree(),'c++lifetree')
