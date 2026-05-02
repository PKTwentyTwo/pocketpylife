'''The code for a Lifetree with a much faster C++ algorithm for simulating OT rules.'''
#Importing modules:
import ast
import ctypes
import hashlib
import os
import subprocess
import sys
import urllib.request
#Other project modules:
try:
    from ..genera.hensel import RuleHandler
except ImportError:
    sys.path.append(os.path.dirname(__file__) + '/../genera')
    from hensel import RuleHandler
try:
    from ..pattern.pattern import Pattern
except ImportError:
    sys.path.append(os.path.dirname(__file__)+'/../pattern')
    from pattern import Pattern
try:
    from .compilecontrol import compilerule
except ImportError:
    from compilecontrol import compilerule
try:
    from ..gridops import *
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from gridops import *
#A few global variables:
CATAGOLUE_URL = 'https://catagolue.hatsya.com'
cppdir = os.path.dirname(__file__)
class Lifetree:
    '''Simulates patterns in outer-totalistic rules using automatically generated C++ code.
Requires a C++ compiler, and requires MinGW to be installed if on Windows.'''
    def __init__(self, rule='b3s23'):
        self.rulehandler = RuleHandler()
        self.rule = self.rulehandler.canoniserule(rule)
        simfile = cppdir + '/lib/' + self.rule + '.so'
        if not os.path.isfile(simfile):
            compilerule(self.rule)
        self.cdll = ctypes.CDLL(simfile)
        self.conditionset = self.rulehandler.makeconditionset(self.rule)
        self.__file__ = __file__
        self.layers = 1
    def getneighbours(self, grid):
        '''For each cell with at least one live neighbour, get a 9-bit integer.'''
        neighbours = {}
        for x in grid:
            xcor, ycor = x[0], x[1]
            for a in range(3):
                for b in range(3):
                    coord = (xcor + a - 1, ycor + b - 1)
                    if coord not in neighbours:
                        neighbours[coord] = 0
                    neighbours[coord] += 2**(8 - 3 * b - a)
        return neighbours
    def advanceone(self, grid):
        '''Advance a grid of cells by one generation.'''
        neighbours = self.getneighbours(grid)
        newgrid = {}
        for x in neighbours:
            if neighbours[x] in self.conditionset:
                newgrid[x] = 1
        return newgrid
    def advancenormal(self, grid, gens):
        '''Advance a grid a specific number of generations.'''
        adv = self.advanceone
        for _ in range(gens):
            grid = adv(grid)
        return grid
    def topayload(self, grid, gens):
        '''Converts a grid to payload.'''
        payload = [str(len(grid)*2).encode('utf-8'), str(gens).encode('utf-8')]
        for x in grid:
            payload += [str(x[0]).encode('utf-8'), str(x[1]).encode('utf-8')]
        return payload
    def cppadvance(self, grid, gens):
        '''Advances a grid by making a call to a shared library.'''
        array = []
        for x in grid:
            array.append(x[0])
            array.append(x[1])
        carray = (ctypes.c_int32 * len(array))(*array)
        wd = os.getcwd()
        os.chdir(cppdir)
        self.cdll.pyadvance(ctypes.c_int32(len(array)), ctypes.c_int32(gens), carray)
        os.chdir(wd)
        with open(cppdir + '/outfile.txt', 'r', encoding='utf-8') as f:
            newgrid = f.read()
        return ast.literal_eval(newgrid)
    def advance(self, grid, gens):
        '''Advances a grid, making decisions about which method to use.'''
        if gens <= 10:
            return self.advancenormal(grid, gens)
        return self.cppadvance(grid, gens)
    def rle_to_grid(self, rle):
        '''Converts an RLE to a dictionary format.'''
        x = 0
        y = 0
        grid = {}
        position = -1
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        cstring = ''
        isnum = False
        while position + 1 < len(rle):
            position += 1
            if not isnum:
                if rle[position] == '#' or rle[position] == 'x':
                    while rle[position] != '\n' and position < len(rle) - 1:
                        position += 1
                    continue
                if rle[position] in digits:
                    isnum = True
                    cstring = rle[position]
                else:
                    operator = rle[position]
                    if operator == '\n':
                        continue
                    if cstring != '':
                        try:
                            integer = int(cstring)
                        except ValueError:
                            raise Warning('Invalid RLE format, defaulting to empty pattern...')
                            return {}
                    else:
                        integer = 1
                    if operator ==  'o':
                        for n in range(integer):
                            grid[(x+n, y)] = 1
                        x += integer
                    elif operator ==  'b':
                        x += integer
                    elif operator ==  '$':
                        x = 0
                        y += integer
                    elif operator ==  '!':
                        break
                    cstring = ''
            else:
                if rle[position] not in digits:
                    isnum = False
                    position -= 1
                else:
                    if rle[position] != '\n':
                        cstring += rle[position]
        return grid
    def grid_to_rle(self, grid, bbox):
        '''Converts a grid to the RLE of a pattern.'''
        rows = {}
        for x, y in grid:
            if y not in rows:
                rows[y] = []
            rows[y].append(x)
        for x in rows:
            rows[x] = sorted(rows[x])
        rows = dict(sorted(rows.items()))
        rle = 'x = '+str(bbox[2])+', y = '+str(bbox[3])+', rule = '+self.rule.replace('b', 'B').replace('s', '/S')+'\n'
        for x in range(bbox[1], bbox[1] + bbox[3]):
            if x not in rows:
                rle += '$'
                continue
            for y in range(bbox[0], bbox[0] + bbox[2]):
                if y in rows[x]:
                    rle += 'o'
                else:
                    rle += 'b'
            rle += '$'
        rle = rle[:-1]
        rle += '!'
        #Compress the RLE:
        operators = ['o', 'b', '$']
        for x in operators:
            longestchain = 1
            while rle.count(x * (longestchain+1)) > 0:
                longestchain += 1
            if longestchain >= 2:
                for n in range(longestchain, 1, -1):
                    rle = rle.replace(x * n, str(n)+x)
        return rle
    def hashsoup(self, instring, sym):
        '''Generates a soup based on the instring, returning a Pattern.'''
        #I borrowed this function from apgsearch Py3 - see the repo (https://github.com/PKTwentyTwo/apgsearch-Py3) for the credits for this function.
        if sym[0] in ['G', 'H'] and 'stdin' not in sym.lower() and len(sym) > 1:
            sym = sym[0].replace('G', 'C').replace('H', 'D') + sym[1:]
            #Adaptation to account for GPU symmetries.
        if 'stdin' not in sym.lower():
            s = hashlib.sha256(instring.encode('utf-8')).digest()
            thesoup = []
            if sym in ['D2_x', 'D8_1', 'D8_4']:
                d = 1
            elif sym in ['D4_x1', 'D4_x4']:
                d = 2
            else:
                d = 0
            for j in range(32):
                t = s[j]
                for k in range(8):
                    if sym in ['8x32']:
                        x = k + 8*(j % 4)
                        y = int(j / 4)
                    elif sym in ['4x64']:
                        x = k + 8*(j % 8)
                        y = int(j / 8)
                    elif sym in ['2x128']:
                        x = k + 8*(j % 16)
                        y = int(j / 16)
                    elif sym in ['1x256']:
                        x = k + 8*(j % 32)
                        y = int(j / 32)
                    else:
                        x = k + 8*(j % 2)
                        y = int(j / 2)
                    if (t & (1 << (7 - k))):
                        if (d == 0) | (x >= y):
                            thesoup.append(x)
                            thesoup.append(y)
                        elif sym in ['D4_x1']:
                            thesoup.append(y)
                            thesoup.append(-x)
                        elif sym in ['D4_x4']:
                            thesoup.append(y)
                            thesoup.append(-x-1)
                        if (sym in ['D4_x1']) & (x == y):
                            thesoup.append(y)
                            thesoup.append(-x)
                        if (sym in ['D4_x4']) & (x == y):
                            thesoup.append(y)
                            thesoup.append(-x-1)
            # Checks for diagonal symmetries:
            if (d >= 1):
                for x in range(0, len(thesoup), 2):
                    thesoup.append(thesoup[x+1])
                    thesoup.append(thesoup[x])
                if d == 2:
                    if sym == 'D4_x1':
                        for x in range(0, len(thesoup), 2):
                            thesoup.append(-thesoup[x+1])
                            thesoup.append(-thesoup[x])
                    else:
                        for x in range(0, len(thesoup), 2):
                            thesoup.append(-thesoup[x+1] - 1)
                            thesoup.append(-thesoup[x] - 1)
            # Checks for orthogonal x symmetry:
            if sym in ['D2_+1', 'D4_+1', 'D4_+2']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(thesoup[x])
                    thesoup.append(-thesoup[x+1])
            elif sym in ['D2_+2', 'D4_+4']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(thesoup[x])
                    thesoup.append(-thesoup[x+1] - 1)
            # Checks for orthogonal y symmetry:
            if sym in ['D4_+1']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(-thesoup[x])
                    thesoup.append(thesoup[x+1])
            elif sym in ['D4_+2', 'D4_+4']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(-thesoup[x] - 1)
                    thesoup.append(thesoup[x+1])
            # Checks for rotate2 symmetry:
            if sym in ['C2_1', 'C4_1', 'D8_1']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(-thesoup[x])
                    thesoup.append(-thesoup[x+1])
            elif sym in ['C2_2']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(-thesoup[x])
                    thesoup.append(-thesoup[x+1]-1)
            elif sym in ['C2_4', 'C4_4', 'D8_4']:
                for x in range(0, len(thesoup), 2):
                    thesoup.append(-thesoup[x]-1)
                    thesoup.append(-thesoup[x+1]-1)
            # Checks for rotate4 symmetry:
            if (sym in ['C4_1', 'D8_1']):
                for x in range(0, len(thesoup), 2):
                    thesoup.append(thesoup[x+1])
                    thesoup.append(-thesoup[x])
            elif (sym in ['C4_4', 'D8_4']):
                for x in range(0, len(thesoup), 2):
                    thesoup.append(thesoup[x+1])
                    thesoup.append(-thesoup[x]-1)
            thesoup2 = {}
            for x in range(len(thesoup)//2):
                thesoup2[(thesoup[2*x], thesoup[2*x+1])] = 1
            return self.pattern(thesoup2)
        if instring.count('-') == 1:
            rle = instring.split('-')[1]
            return self.pattern(rle)
        return self.pattern('b!')
    def download_synth(self, apgcode):
        '''Downloads a glider synthesis from Catagolue.'''
        if self.rule != 'b3s23':
            raise ValueError('Can only download syntheses if configured for b3s23.')
        with urllib.request.urlopen(CATAGOLUE_URL+'/textsamples/'+apgcode+'/'+'b3s23/synthesis') as c:
            response = c.read().decode('utf-8')
        if 'x' in response:
            return response
        return None
    def download_soups(self, apgcode, sym='C1'):
        '''Returns a list of soups producing a target object.'''
        with urllib.request.urlopen(CATAGOLUE_URL + '/textsamples/' + apgcode + '/' + self.rule) as c:
            response = c.read().decode('utf-8')
        soups = []
        for x in response.split('\n'):
            data = x.split('/')
            if len(data) != 2:
                continue
            symmetry, seed = data[0], data[1]
            if symmetry != sym:
                continue
            soups.append(self.hashsoup(seed, symmetry))
        return soups
    def pattern(self, data):
        '''Creates a new Pattern given an RLE string.'''
        datatype = identifytype(data)
        if datatype == 'rle':
            grid = self.rle_to_grid(data)
        elif datatype == 'apgcode':
            grid = apgcodetogrid(data)
        else:
            grid = data
        pt = Pattern(self, grid)
        return pt
