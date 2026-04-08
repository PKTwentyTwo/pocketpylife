'''The code for the Pattern class used for high-level manipulation with multistate rules.'''
import copy
import math
import hashlib
import os
try:
    from ..gridops import *
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from gridops import *
try:
    from ..viewer import sim
except ImportError:
    try:
        from viewer import sim
    except ImportError:
        #Tkinter is probably not installed.
        def sim(pt, gens, arguments = {}):
            return None
class Pattern:
    '''This is the class used for manipulation of patterns.'''
    def __init__(self, lifetree, grid=dict()):
        '''This method should only be called by a lifetree.'''
        self.lifetree = lifetree
        self.grid = grid
    def __getitem__(self, gens):
        '''Advances a pattern a given number of generations.'''
        self2 = self.clone()
        self2.grid = self2.lifetree.advance(self.grid, gens)
        return self2
    def __call__(self, *args):
        '''Translates or transforms a pattern.'''
        if len(args) == 2:
            return self.move(args[0], args[1])
        if len(args) == 1:
            return self.transform(args[0])
        raise TypeError('Expected at most 2 arguments, received '+str(len(args))+'.')
    def __or__(self, other):
        '''Returns the OR of two patterns.'''
        if type(self) != type(other):
            raise TypeError('Can only perform logical operations with other instances of Pattern.')
        cells = applyop(self.grid, other.grid, 'add')
        return self.lifetree.pattern(cells)
    def __add__(self, other):
        '''Returns the OR of two patterns.'''
        return self.__or__(other)
    def __xor__(self, other):
        '''Returns the XOR of two patterns.'''
        if type(self) != type(other):
            raise TypeError('Can only perform logical operations with other instances of Pattern.')
        cells = applyop(self.grid, other.grid, 'xor')
        return self.lifetree.pattern(cells)
    def __sub__(self, other):
        '''Removes live cells in one pattern from the other.'''
        if type(self) != type(other):
            raise TypeError('Can only perform logical operations with other instances of Pattern.')
        cells = applyop(self.grid, other.grid, 'sub')
        return self.lifetree.pattern(cells)
    def __ixor__(self, other):
        '''Returns the XOR of two patterns.'''
        return self.__xor__(other)
    def __eq__(self, other):
        '''Checks if two patterns are equal, including their location.'''
        if type(self) != type(other):
            return False
        if self.digest != other.digest:
            return False
        if (self - other).population != 0:
            return False
        if (other - self).population != 0:
            return False
        return True
    def transform(self, transformation):
        '''Transforms a pattern relative to the origin.'''
        pt2 = self.clone()
        pt2.grid = transformgrid(self.grid, transformation)
        return pt2
    def centre(self):
        '''Moves a pattern so that the bounding box is centered on the origin.'''
        bbox = self.bbox
        dx = -math.floor((bbox[0] + bbox[2])/2)
        dy = -math.floor((bbox[1] + bbox[3])/2)
        return self(dx, dy)
    def clone(self):
        '''Creates a copy of a pattern.'''
        thecopy = copy.deepcopy(self)
        thecopy.cleanup()
        return thecopy
    def cleanup(self):
        '''Cleans up the stored data of a pattern.'''
        self.grid = cleanupgrid(self.grid)
    def move(self, dx, dy):
        '''Translates a pattern by (dx, dy).'''
        self2 = self.clone()
        self2.grid = shiftgrid(self.grid, dx, dy)
        self2.cleanup()
        return self2
    def oscar(self, maxgens=1024):
        '''Finds the period of a pattern. Returns an error if it is aperiodic.'''
        inithash = self.digest
        pt = self.clone()[1]
        gens = 1
        while pt.digest != inithash:
            pt = pt[1]
            gens += 1
            if gens > maxgens:
                raise ValueError('Pattern does not become periodic within '+str(maxgens)+' generations.')
                return -1
        return gens
    def save(self, filename = 'pattern.rle'):
        '''Saves the RLE of a pattern in a file.'''
        rle = self.rle
        f = open(filename, 'w', encoding = 'utf-8')
        f.write(rle)
        f.close()
    @property
    def rle(self):
        '''The Run Length Encoding (RLE) of a pattern.'''
        self.cleanup()
        return self.lifetree.grid_to_rle(self.grid, self.bbox)
    @property
    def population(self):
        '''How many live cells a pattern has.'''
        self.cleanup()
        return len(self.grid)
    @property
    def coords(self):
        '''A list of every cell in a pattern.'''
        self.cleanup()
        thecoords = []
        for x in self.grid:
            thecoords.append(x)
        return thecoords
    @property
    def firstcell(self):
        '''The first cell of a pattern.'''
        self.grid = dict(sorted(self.grid.items()))
        count = 0
        for x in self.grid:
            count += 1
            if count == 1:
                return x
        return None
    def viewer(self, gens=1, options={}):
        '''Opens a Tkinter window showing the pattern.'''
        sim(self, gens, options)
    @property
    def digest(self):
        '''A hash of the pattern (orientation dependent).'''
        return calcdigest(self.grid)
    @property
    def octodigest(self):
        '''A hash of the pattern (orientation independent).'''
        return calcoctodigest(self.grid)
    @property
    def period(self):
        '''The period of a pattern. Returns an error if aperiodic.'''
        return self.oscar()
    @property
    def displacement(self):
        '''The displacement of a periodic pattern in the form (dx, dy). Returns an error if aperiodic.'''
        period = self.period
        if self.population == 0:
            raise ValueError('Cannot calculate displacement for an empty pattern.')
        firstcella = self.firstcell
        firstcellb = self[period].firstcell
        displacement = (firstcellb[0] - firstcella[0], firstcellb[1] - firstcella[1])
        return displacement
        
    @property
    def bbox(self):
        '''The bounding box of a pattern in the form [x, y, dx, dy].'''
        cells = self.coords
        if len(cells) == 0:
            #Empty patterns do not have a proper bounding box.
            return None
        exes = [c[0] for c in cells]
        whys = [c[1] for c in cells]

        x = min(exes)
        y = min(whys)
        dx = max(exes) - x + 1
        dy = max(whys) - y + 1
        return [x, y, dx, dy]
    @property
    def components(self):
        '''A list of the connected islands in a pattern.'''
        coords = self.coords
        islands = []
        while len(coords) > 0:
            coord = coords[0]
            island = [coord]
            coords.remove(coord)
            chosencoord = 0
            while chosencoord < len(island):
                coord = island[chosencoord]
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        neighbour = (coord[0] + dx, coord[1] + dy)
                        if neighbour in coords and neighbour not in islands:
                            coords.remove(neighbour)
                            island.append(neighbour)
                chosencoord += 1
            islands.append(island)

        islands2 = []
        for x in islands:
            current_island = {}
            for y in x:
                current_island[y] = 1
            islands2.append(self.lifetree.pattern(current_island))
        return islands2
    @property
    def apgcode(self):
        '''A unique identifier for periodic patterns.'''
        try:
            period = self.period
        except:
            return 'aperiodic'
        pt = self.clone()
        gridphases = []
        for x in range(period):
            gridphases.append(pt.grid)
            pt = pt[1]
        gridphases2 = []
        for x in gridphases:
            gridphases2 += getorientations(x)
        canonicalapgcode = 'Z'*10000
        for x in gridphases2:
            canonicalapgcode = compareapgcode(canonicalapgcode, getgridapgcode2(x, self.lifetree.layers))
        if period == 1:
            prefix = 'xs' + str(self.population) + '_'
        else:
            if self.displacement != (0, 0):
                prefix = 'xq' + str(period) + '_'
            else:
                prefix = 'xp' + str(period) + '_'
        
        return prefix + canonicalapgcode
