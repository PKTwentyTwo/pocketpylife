'''Tests the Tkinter viewer for patterns.'''
import os
import sys
try:
    from ..whichtree import lifetree
except:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from whichtree import lifetree
try:
    from ..viewer import sim
except:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from viewer import sim
lt = lifetree('b3s23History')
pt = lt.pattern('''x = 31, y = 42, rule = B3/S23
12b2o$12bobo$14b3o$13bo3bo$13b2ob2o2$11bo7bo$11bo7bo$11bo7bo7$14b3o$2o
12b3o12b2o$2o11bo3bo11b2o$13b2ob2o5$13b2ob2o$2o11bo3bo11b2o$2o12b3o12b
2o$14b3o7$11bo7bo$11bo7bo$11bo7bo2$13b2ob2o$13bo3bo$14b3o$16bobo$17b2o
!''')
print(lt.__file__)
pt = pt[44]
pt.viewer(44, {'fps':22})

#sim(pt, 44, {'fps':22})
