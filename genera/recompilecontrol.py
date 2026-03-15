'''Responsible for determining if new rules need to be compiled.'''
import json
import os
import hashlib
datafile = os.path.dirname(__file__) + '/ruletables.json'
if not os.path.isfile(datafile):
    f = open(datafile, 'w', encoding = 'utf-8')
    f.write('{}')
    f.close()
try:
    with open(datafile, 'r', encoding='utf-8') as f:
        ruletables = json.loads(f.read())
except:
    print('Error while decoding list of JSON ruletables!')
    f = open(datafile, 'w', encoding = 'utf-8')
    f.write('{}')
    f.close()    
def checksum(file):
    '''Calculates a file's SHA256 checksum.'''
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()
def addrule(filepath):
    '''Adds a filepath to the list of ruletables and their hashes.'''
    filepath = filepath.replace('\\', '/')
    ruletables[filepath] = checksum(filepath)
    with open(datafile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(ruletables))
def needsrecompile(filepath):
    '''Returns True if a rule requires recompilation.'''
    filepath = filepath.replace('\\', '/')
    if filepath not in ruletables:
        addrule(filepath)
        return True
    oldchecksum = ruletables[filepath]
    newchecksum = checksum(filepath)
    if oldchecksum == newchecksum:
        #File has not changed; don't recompile.
        return False
    addrule(filepath)
    return True


