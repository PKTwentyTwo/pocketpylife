'''The viewer window for patterns.'''
from tkinter import Tk, Canvas
import time
import random
def preproc(pt, gens):
    '''Simulates a pattern and saves the grids ahead of time.'''
    grids = []
    for x in range(gens):
        grids.append(pt.grid)
        pt = pt[1]
    return grids
def getmaxpop(grids):
    '''Returns the maximum population of the grids, to know how many squares are needed.'''
    maxpop = 0
    for x in grids:
        maxpop = max(maxpop, len(x))
    return maxpop
def gettotalarea(grids):
    '''Returns the total bounding box of the phases.'''
    minx = 99999999
    miny = 99999999
    maxx = -99999999
    maxy = -99999999
    for g in grids:
        for x, y in g:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    return (minx, miny, maxx - minx + 1, maxy - miny + 1)
def arrangegeneration(canvas, grids, gen, squares, dx, dy, squaresize, colours):
    '''Arranges the squares as required to display a generation.'''
    generation = grids[gen]
    count = 0
    for x in generation:
        square = squares[count]
        canvas.moveto(square, (x[0] + dx) * squaresize,(x[1] + dy) * squaresize)
        canvas.itemconfig(square, fill=colours[generation[x]])
        count += 1
    while count < len(squares):
        canvas.moveto(squares[count], 10000, 10000)
        count += 1
def sim(pt, gens, arguments = {}):
    '''Simulates a pattern.'''
    window = Tk()
    window.title('Viewer')
    screenx, screeny = window.winfo_screenwidth(), window.winfo_screenheight()
    squares = []
    grids = preproc(pt, gens)
    maxpop = getmaxpop(grids)
    bbox = gettotalarea(grids)
    dx, dy = -bbox[0], -bbox[1]
    squaresize = min(screenx // bbox[2], screeny // bbox[3])
    squaresize = round(squaresize * 0.9)
    window.minsize(bbox[2] * squaresize, bbox[3] * squaresize)
    canvas = Canvas(window, width = bbox[2] * squaresize, height = bbox[3] * squaresize)
    canvas.pack()
    #Set up colours:
    layers = pt.lifetree.layers
    colours = {0:'black'}
    if layers == 1:
        colours[1] = 'white'
    elif pt.lifetree.rule.endswith('History'):
        #These are the standard colours for (Rule)History rules:
        colours[0] = 'black'
        colours[1] = '#00FF00' #Green.
        colours[2] = '#000080' #A dark blue.
        colours[3] = '#A8FFA8' #A shade of white.
        colours[4] = '#FF0000' #Red.
        colours[5] = '#FFFF00' #Yellow
        colours[6] = '#606060' #A dark grey.
    elif pt.lifetree.genera == 'generations':
        #Generations states are a smooth gradient from red to yellow.
        #Red is #FF0000, yellow is #FFFF00, so numbers from 0 to 255 are generated for the G value.
        for x in range(1, layers + 1):
            colour = '#FF'
            gradient = round(((x - 1) / (layers - 1)) * 255)
            greenpart =  str(hex(gradient))[2:].upper()
            if len(greenpart) == 1:
                greenpart = '0' + greenpart
            colour += greenpart + '00'
            colours[x] = colour
    else:
        #Generating random hex codes works well as a fallback:
        for x in range(1, layers + 1):
            colour = '#'
            for _ in range(6):
                colour += str(hex(random.randint(0, 15)))[2:].upper()
            colours[x] = colour
    #Interpret variables:
    if 'fps' in arguments:
        fps = int(arguments['fps'])
    else:
        fps = 30
    secondsperframe = 1 / fps
    if 'loops' in arguments:
        maxloops = int(arguments['loops'])
        if maxloops < 0:
            maxloops = 10**12
    else:
        maxloops = 10**12 #At 1000 fps, this would take 31 years to complete, so I think it's enough.
    if 'bg' in arguments:
        colours[0] = arguments['bg']
    if 'fg' in arguments:
        colours[1] = arguments['fg']
    canvas.config(background = colours[0])
    for x in range(maxpop):
        squares.append(canvas.create_rectangle(10000, 10000, 10000 + squaresize, 10000 + squaresize, fill = 'black'))
    loops = 0
    while True:
        try:
            for n in range(gens):
                starttime = time.time()
                arrangegeneration(canvas, grids, n, squares, dx, dy, squaresize, colours)
                window.update()
                timetowait = max(secondsperframe, 0)
                time.sleep(timetowait)
            loops += 1
            if loops >= maxloops:
                break
        except Exception as e:
            break

