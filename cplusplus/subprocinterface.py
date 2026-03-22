import subprocess
import os
import time
testgrid = {(1, 0): 1, (0, 1): 1, (2, 1): 1, (1, 2): 1, (8, 10): 1, (6, 11): 1, (8, 11): 1, (5, 12): 1, (6, 12): 1, (8, 12): 1, (4, 14): 1, (5, 14): 1, (6, 14): 1}
def topayload(grid, gens):
    '''Converts a grid to payload.'''
    payload = [str(len(grid)*2).encode('utf-8'), str(gens).encode('utf-8')]
    for x in grid:
        payload += [str(x[0]).encode('utf-8'), str(x[1]).encode('utf-8')]
    return payload
def advance(grid, gens):
    proc = subprocess.Popen([os.getcwd() + '/life3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    payload = topayload(grid, gens)
    for x in payload:
        proc.stdin.write(x + b'\n')
        proc.stdin.flush()
    output = proc.stdout.read().decode('utf-8')
    output = output.split('\n')
    newgrid = {}
    for x in range(len(output) // 2):
        newgrid[int(output[2*x]), int(output[2*x+1])] = 1
    return newgrid
starttime = time.time()
for x in range(1):
    testgrid = advance(testgrid, 29055)
print(time.time() - starttime)
print(len(testgrid))
