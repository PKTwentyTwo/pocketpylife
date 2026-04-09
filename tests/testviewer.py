'''Tests the Tkinter viewer for patterns.'''
import os
import sys
import time
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
lt = lifetree('b3s23history')
print(lt.__file__)
pt = lt.pattern('''x = 86, y = 137, rule = B3/S23
51b2o$50bobo$44b2o4bo$42bo2bo2b2ob4o$42b2obobo3bo2bo$45bobobobo$45bob
ob2o$46bo2$59b2o$50bo8bo$50b2o5bobo$57b2o$44bo$43bo$43b3o4$47b2o$48bo
$45b3o10bo$45bo11b2o$57bobo5$30bo$28b2o$29b2o3$81b2o$9bo71bo$9b3o59b2o
10bo$12bo50b2o5b3o6b5o$11b2o51bo6bobo4bo$64bobo3b4o5b3o$65b2o3b3ob2o6b
o$3b2o64bo2bobo2b6o$3bo65bo2bo2bob3o3b2o$2obo65b2o3bo2bo2b3o2bo$o2b3o
4b2o2bo59b2o6bob2o$b2o3bo3b2o2bobo36bo14bo2b3o8bo$3b4o7b2o28bo8b3o12b
o4bo7b2o$3bo15b2o23b3o9bo$4b3o12bobo2b2o21bo7b2o13bo3bo$7bo13bo2bo21b
2o26bo$2b5o14b2obo36bo11bo$2bo19bob2o2b2o30b3o11b3o$4bo17bo4bobo29b2o
bo13bo$3b2o18b3obo30b2o$25bob2o29b2o$69bo$45b2o21bobo$44b2ob2o15bo6bo
$21bobo5b2o3b2o8b2ob2o15b4o2bo$22b2o6b2o2b2o10b3o12bo6b2o$22bo6bo30b2o
bo4bo9b2o$61b4o2bo9bobo$57b2o4b3o12bo$43bo3b2o7bobo$42bobo3bo7bo$41bo
bo3bo7b2o$41bo4bo$29b2obo7b2o5b3o$7b2o20b2ob3o14bo$8bo26bo38b2o4b2obo
$6bo22b2ob3o37b2o2bo3bob2o$6b5o14b2o3bobo40bob2o$11bo13bo4bobo37b2ob2o
$8b3o6b3o3bobo5bo38b3o$7bo8bo3bo2b2o45bo$7b4o4bo5bo48b2o2bo$5b2o3bo4b
o5bo49b3o$4bo2b3o5bo5bo50bo$4b2obo8bo3bo$7bo9b3o$7b2o2$36bo$15b2o17b3o
$16bo16bo29bo$13b3o17b2o28b3o$13bo16bo35bo$29b2o6b2o26bobo$29bobo4bo2b
o26bo4b3o9b2o$36b2obo31bo11bo$19b2o18b2o23bo7bo8bobo$20bo15b2o3bo21bo
bobo9bo3b2o$20bobo12bo2b3o22bo2b2o7bo2bo$21b2o11bob2o24b2o10bo4bo$26b
2o7bo2bo34bo5bo$24b2o11b2o37b2ob2o$20bo3b2ob3o44bob2o$19bobo3b2ob3o43b
o2b2o5b2o$19bo5bo3bo45b3o6bo$20bo3b4obo35bo10bo5bobo$21bo7bo35b3o14b2o
$23bobob2o39bo$24b2ob2o38b2o$10bo15bo44bo$10b3o19b2o36bobo$13bo4b2o12b
o37bo2bo$12b2o5b2o12b3o35b2o$18bo6b2o8bo$8b2o15b2o$7bo2bo$7bob2o27bo33b
o12bo$6b2o18b2o10b3o30bob2o8bobo$5bo3b2o15bo14bo28b2o3bo8b2o$6b3o2bo12b
obo13bo25b2o3bo$9b2obo11b2o14bo2bo2bobo11b2o5b2o2bo3bo$8bo2bo8b2o21bo
20b2obo3bo$8b2o10b2o8bo6b2o2bo2b2o11bo6bo6bo$30b3o4b2o5b4o10bo5bobo$26b
2o5bo11bo7bo3bobo5b2o5b2o$17bo8b2o4b2o6bo3bo8bo$17bo$18bo4bo16b3o26bo
$16b2o5bo10b2o11b2o19bobo$16bobo15b2o12bo20b2o$60b2o$13b2o3bo6bo14bob
obo16bo$14bo23b2obo18bo$11b3o27b2o17b2o$11bo9bo$20b2o22b2o$24b2o18bob
o$23bobo7bo12bo$23bo8bobo11b2o$22b2o4b2obobo$27bobobobobo$27bo4bobobo
$28b3obobobo$30b2o3bo!''')
pt = pt[59]
#pt.viewer(44, {'fps':22})
starttime = time.time()
sim(pt, 59, {'fps':1380})
timetaken = time.time() - starttime
print('Simulated pattern in '+str(round(timetaken, 3))+' seconds.')
