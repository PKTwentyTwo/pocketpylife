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
#Test the other genera:
lt3 = pocketpylife.lifetree('b3s23-a5')
lt4 = pocketpylife.lifetree('B3/S23/C3')
lt5 = pocketpylife.lifetree('LifeHistory.rule')
pt3 = lt3.pattern('xq4_27')
pt4 = lt4.pattern('''x = 24, y = 27, rule = 23/3/3
.3A9.3A$A2BA9.A2BA$AB2.BA5.AB2.BA$2.A2BA5.A2BA$2.A2BA5.A2BA2$6.2A.2A$
5.A.A.A.A$5.A.A.A.A$4.2A.A.A.2A8.A$5.B.A.A.B8.3A$4.2B.B.B.2B6.A2.2A$4.
3A3.3A5.4AB$19.2A11$10.2A$9.A.A$10.A!
''')
pt5 = lt.pattern('''x = 47, y = 39, rule = LifeHistory
16.2A$17.A$16.A9.A13.C$16.4A4.3A12.C2B$19.A3.A14.B3C$14.3AB5.2A12.4B$
13.A2.AB2.5B11.4B$13.2A2.6B12.4B$17.7B10.4B$16.3B2A3B9.4B$16.3B2A5B6.
4B$17.10B4.4B$11.2B.3D2.7B.B2.4B$10.3BD3BD.14B$10.3BD3BD14B$9.4BD3BD14B
$8.6B3D17B$8.27B$7.29B$8.27B$8.26B$8.26B$9.24B.2B$8.30B3.B$7.29B2AB.B
2A$7.14B2A11B.A2BA2B2A$7.14B2A13BABA3B$5.2A30BA4B$5.2A14B5.7B8.B$4.16B
6.6B3.A4.2A.A$5.12B10.3B4.A.A3.2AB3A$6.3B2A2B.2B11.5B3.A5.B4.A$4.4BA2B
A2B16.2A8.2A.3A$4.5BABA2B16.A10.A.A$4.6BAB.B2A15.3A7.A.A$2.2AB.5B2.BA
.A16.A8.A$.A.AB.4B6.A$.A14.2A$2A!
''')
try:
    lt6 = pocketpylife.cpplifetree('b2s')
    pt = lt6.pattern('xs4_33')
    if pt[200].population != 16644:
        raise ValueError('Error with C++ lifetree simulation!')
except Exception as e:
    print('Error occurred while attempting to test C++ lifetree:')
    print(e)
print('Concluded testing with no errors.')
