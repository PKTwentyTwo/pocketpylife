'''Handles the parsing of custom rules.'''
import os
import itertools
workingdir = os.path.dirname(__file__)
def istransition(line, knownvars=dict()):
    '''Determines whether a line is likely to be specifying a transition.'''
    characters = [x for x in knownvars]
    characters += [' ', ',']
    characters += [str(x) for x in range(10)]
    for n in line:
        if n not in characters:
            return False
    if line.count(',') != 9:
        return False
    return True
def parsetable(table):
    '''Parses a ruletable.'''
    lines = table.split('\n')
    section = 'NONE'
    name = 'testrule'
    globalvars = {'n_states':2, 'neighborhood':'Moore','symmetries':'permute'}
    statevars = {}
    transitions = []
    linenum = -1
    try:
        for x in lines:
            linenum += 1
            if x == '':
                #Empty line: skip
                continue
            if x[0] == '#':
                #Comment line, skip.
                continue
            if x[0] == '@':
                #Line specifies a property or section
                if ' ' in x:
                    propertyname = x[1:x.find(' ')]
                else:
                    propertyname = x[1:]
                section = propertyname
                if section == 'RULE':
                    name = x.replace('@RULE', '').replace(' ', '')
                continue
            if section in ['ICONS', 'COLORS']:
                #Don't worry about these.
                continue
            if x.count(':') == 1 and section not in ['NONE', 'RULE', 'ICONS', 'COLORS'] :
                #Global variable line, probably.
                splitline = x.split(':')
                varname = splitline[0]
                value = splitline[1]
                if varname == 'neighborhood' and value.lower().replace(' ', '') != 'moore':
                    raise ValueError('A Lifetree can only simulate Moore neighbourhood rules.')
                globalvars[varname] = value
                continue
            if x.startswith('var') and section in ['TREE', 'TABLE']:
                #State variable. These need to be used when generating the iteration set.
                varname = x[x.find(' ')+1:x.find('=')].replace(' ', '')
                if x.count('{') > 0:
                    statetext = x[x.find('{')+1:x.find('}')]
                else:
                    statetext = x[x.find('=')+1:].replace(' ', '')
                statevalues = statetext.split(',')
                statevars[varname] = statevalues
                continue
            if istransition(x, statevars):
                #Transition specification detected.
                line = x.replace(' ', '')
                spec = line.split(',')
                transitions.append(spec)
                if len(spec) != 10:
                    raise ValueError('Error on line ' + str(linenum) + ': Did not specify 10 states.')
                continue
    except Exception as e:
        raise SyntaxError('The following error occurred on line ' + str(linenum) + ':\n' + str(e))
    statevars = assign(statevars)
    code = '\'\'\'Automatically generated function for simulating custom rule \"' + name + '\".\'\'\'\n' + generatecode(globalvars, statevars, transitions)
    f = open(workingdir + '/customrulesim.py', 'w', encoding='utf-8')
    f.write(code)
    f.close()
    return (name, globalvars['n_states'])
def isvalidvar(statevars):
    '''Determines whether a set of state variables is valid.'''
    for x in statevars:
        for y in statevars[x]:
            if not y.isnumeric():
                return False
    return True
def assign(statevars):
    '''Ensures that all state variables are numeric lists.'''
    loops = 0
    while not isvalidvar(statevars):
        for x in statevars:
            for y in statevars[x]:
                if not y.isnumeric():
                    variable = y
                    statevars[x].remove(y)
                    statevars[x] += statevars[y]
        loops += 1
        #Raise an error if stuck in what is probably an inescapable loop:
        if loops > 256:
            raise ValueError('Infinite loop detected while parsing variables from ruletable!')
    return statevars
def rotate(t):
    '''Rotates a set of states 90* clockwise.'''
    m = t[1:9]
    newouter = [m[6], m[7], m[0], m[1], m[2], m[3], m[4], m[5]]
    new = t[0:1] + newouter + t[9:]
    return new
def reflect(t):
    '''Reflects a set of states in the x axis.'''
    m = t[1:9]
    newouter = [m[4], m[3], m[2], m[1], m[0], m[7], m[6], m[5]]
    new = t[0:1] + newouter + t[9:]
    return new
def permute(transition):
    '''Permutes a transition.'''
    modify = transition[1:9]
    arrangements = list(itertools.permutations(modify))
    arrangements = [[transition[0]] + list(x) + [transition[9]] for x in arrangements]
    present = set()
    removed = 0
    #Remove duplicates:
    for x in range(40320):
        item = arrangements[x - removed]
        if ''.join(item) not in present:
            present.add(''.join(item))
        else:
            arrangements.pop(x - removed)
            removed += 1
    return arrangements
def rotate8(transition):
    '''Applies the needed operations to a transition to apply rotate8.'''
    modify = transition[1:9]
    retval = []
    for x in range(8):
        newarrangement = []
        for n in range(8):
            newarrangement.append(modify[(n+x)%8])
        retval.append([transition[0]] + newarrangement + [transition[9]])
    return retval
def getorientations(transition, symmetry):
    '''Returns a list of the different orientations of a transition.'''
    if symmetry == 'none':
        return [transition]
    if symmetry == 'permute':
        return permute(transition)
    if symmetry == 'rotate4reflect':
        orientations = []
        for _ in range(2):
            for __ in range(4):
                transition = rotate(transition)
                if transition not in orientations:
                    orientations.append(transition)
            transition = reflect(transition)
        return orientations
    if symmetry == 'rotate8':
        return rotate8(transition)
    if symmetry == 'rotate4':
        orientations = []
        for b in range(4):
            transition = rotate(transition)
            if transition not in orientations:
                orientations.append(transition)
            transition = reflect(transition)
        return orientations
    return getorientations(transition, 'none')
def generatecode(globalvars, statevars, transitions):
    '''Generates Python code to iterate a grid based on the parsed table.'''
    indent = '    '
    code = '''def advancecell(cells):
'''
    cellnames = ['cell' + str(x) for x in range(9)]
    ifstatements = set()
    for transition in transitions:
    #Processes a single transition:
        fulltransition = getorientations(transition, globalvars['symmetries'])
        for t in fulltransition:
            conditional = indent + 'if '
            usedvariables = {}
            for y in range(9):
                cellvalue = t[y]
                #If the value is a number:
                if cellvalue not in statevars:
                    conditional += 'cells[' + str(y)+'] == \''+str(cellvalue)+'\' and '
                    continue
                #If the value is a variable not used so far in the current transition:
                if cellvalue not in usedvariables:
                    usedvariables[cellvalue] = str(y)
                    conditional += 'cells['+ str(y)+'] in '+str(statevars[cellvalue])+' and '
                #If the value is a variable used in the current transition:
                else:
                    conditional += 'cells[' + str(y)+'] == cells[' + str(usedvariables[cellvalue])+'] and '
            #Remove the final and:
            conditional = conditional[:-5] + ':'
            ifstatement = conditional + '\n' + indent * 2
            if t[9] not in statevars:
                ifstatement += 'return '+t[9]
            elif t[9] in usedvariables:
                ifstatement += 'return cells['+usedvariables[t[9]]+']'
            else:
                raise SyntaxError('Error while compiling ruletable: Cannot have variable output with unused variable for a transition.')
            if ifstatement not in ifstatements:
                code += ifstatement + '\n'
                ifstatements.add(ifstatement)
    code += indent + 'return cells[0]'
    return code
def compile_rule(path_to_ruletable):
    '''Compiles a custom rule given the path to the ruletable.'''
    if not os.path.isfile(path_to_ruletable) and not os.path.isfile(workingdir + '/' + path_to_ruletable):
        raise FileNotFoundError('Unable to locate a ruletable at '+str(path_to_ruletable))
    try:
        f = open(path_to_ruletable, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        return parsetable(content)
    except FileNotFoundError:
        f = open(working_dir + '/' + path_to_ruletable, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        return parsetable(content)        
        
compile_rule('B3S23-a5Symbiosis.rule')
