'''Tests the speed using Lidka with various types of Lifetrees.'''
import os
import sys
import time
rootdir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(rootdir + '/cplusplus')
sys.path.append(rootdir + '/cythlib')
sys.path.append(rootdir + '/lifetrees')
try:
    from ..cplusplus.cpplifetree import Lifetree as cpplifetree
except ImportError:
    from cpplifetree import Lifetree as cpplifetree
try:
    from ..cythlib.cython_setup import cython_compile
    cython_compile(False)
    from ..cythlib.cylifetree import Lifetree as cylifetree
except ImportError:
    from cython_setup import cython_compile
    cython_compile(False)
    from cylifetree import Lifetree as cylifetree
try:
    from ..lifetrees.lifetree import Lifetree as lifetree
except:
    from lifetree import Lifetree as lifetree

lidka_rle = '''x = 9, y = 15, rule = B3/S23
bo$obo$bo8$8bo$6bobo$5b2obo2$4b3o!'''
def test(lt, name):
    starttime = time.time()
    pt = lt.pattern(lidka_rle)
    evpt = pt[29055]
    print(evpt.population)
    timetaken = time.time() - starttime
    print(name + ' finished testing in '+str(round(timetaken, 3))+' seconds.')
#test(lifetree(), 'pylifetree')
#test(cylifetree(), 'cylifetree')
test(cpplifetree(),'c++lifetree')
