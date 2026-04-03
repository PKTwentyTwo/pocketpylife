'''A script to test all core components of the module.'''
import os
import sys
#The folder containing pocketpylife is placed first in sys.path so it gets imported first:
sys.path = [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))] + sys.path
import pocketpylife
#Tests with standard life:
lt = pocketpylife.lifetree('b3s23')
print('Lifetree file: '+lt.__file__)
pt = lt.pattern('bo$3o$o!')
if pt.population != 5:
    raise ValueError('Error with RLE parsing; R-pentomino has population '+str(pt.population))
evpt = pt[1103]
if evpt.population != 116:
    raise ValueError('Error with pattern evolution; evolved R-pentomino has population '+str(evpt.population))
components = evpt.components
if len(components) != 25:
    raise ValueError('Error with pattern decomposition; evolved R-pentomino has '+str(len(components))+' components.')
rle = pt.rle
bbox = pt.bbox
#Check rotations:
for orientation in ['flip_x', 'flip_y', 'identity', 'rot_90', 'rot_180', 'rot_270', 'flip_xy', 'rcw', 'rccw']:
    pt.transform(orientation)
print('Successfully tested B3/S23 with no errors.')
#Testing the other components with Pedestrian Life:
lt2 = pocketpylife.lifetree('b38s23')
pt2 = lt2.pattern('''x = 39, y = 22, rule = B38/S23
20b2o$20b2o2$28b2o$26bo2bo$26b3o$27bo3$2o$2o2$8b2o$6bo2bo$6b3o$7bo4$
36b2o$36bobo$37bo!
''')
period = pt2.period
apgcode = pt2.apgcode
displacement = pt2.displacement
if period != 190:
    raise ValueError('Error with period detection; Pedestrian Life ship has period '+str(period))
if apgcode != 'xq190_y533zy8svzzz33zxsvzzyf6a4':
    raise ValueError('Error with apgcode detector; Pedestrian Life ship has apgcode '+apgcode)
print('Successfully tested B38/S23 with no errors.')
#Create the other genera:
lt3 = pocketpylife.lifetree('b3s23-a5')
lt4 = pocketpylife.lifetree('B3/S23/C3')
lt5 = pocketpylife.lifetree('LifeHistory.rule')
print('Concluded testing with no errors.')
