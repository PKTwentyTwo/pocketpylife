'''Responsible for dealing with C++ compilation.'''
import os
import struct
import subprocess
import sys
try:
    from ..genera.hensel import RuleHandler
    from ..genera.findgenera import getgenera
    from .gencode import gencode
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/genera')
    from hensel import RuleHandler
    from findgenera import getgenera
    from gencode import gencode
rh = RuleHandler()
#Flags passed to the compiler:
COMPILER_ARGS = ['-O3', '-pthread', '-march=native', '-Ofast', '-funroll-loops']
def getcompiler():
    '''Determines if it is feasible to compile in the current working environment.
Throws an error if compilation is not possible, and otherwise returns the compiler location.'''
    if os.name == 'nt':
        #Compilation on Windows is not currently supported.
        raise OSError('C++ bindings are currently unavaliable on Windows.')
    #Check if the architecture is 64-bit:
    numbits = 8 * struct.calcsize("P")
    if numbits != 64:
        raise OSError('C++ bindings are currently not avaliable for '+str(numbits)+'-bit systems.')
    #Check that g++ is avaliable:
    try:
        gpp_location = subprocess.check_output(['which', 'g++']).decode('utf-8').replace('\n', '')
    except subprocess.CalledProcessError:
        raise OSError('''g++ does not appear to be installed on this system.
Try installing it with: sudo apt install g++''')
    return gpp_location
def isvalid(rule):
    '''Determines whether a rule is valid or not for code generation.'''
    genera = getgenera(rule)
    return genera in ['b3s23life', 'lifelike']
def compilerule(rule):
    '''Generates and compiles code for a given rule.'''
    if not isvalid(rule):
        raise ValueError('Rule '+rule+' belongs to genus \''+getgenera(rule)+'\' and cannot be compiled.')
    rule = rh.canoniserule(rule)
    cppdir = os.path.dirname(__file__)
    if not os.path.exists(cppdir+'/bin'):
        os.mkdir(cppdir+'/bin')
    #Generate the code:
    code = gencode(rule)
    with open(cppdir + '/life.cpp', 'w', encoding = 'utf-8') as f:
        f.write(code)
    #Write a command to compile the code:
    command = [getcompiler()]
    command += [cppdir+'/life.cpp', '-o', cppdir+'/bin/'+rule]
    command += COMPILER_ARGS
    joinedcommand = ''
    for x in command:
        joinedcommand += x + ' '
    joinedcommand = joinedcommand[:-1]
    print('Attempting compilation with command:\n'+joinedcommand)
    #Compile the code:
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compiler_stdout, compiler_stderr = proc.communicate()
    status = proc.returncode
    if status == 0:
        print('Compilation successful.')
        os.remove(cppdir+'/life.cpp')
    else:
        raise ValueError('Error occurred during compilation!\n\n' + compiler_stderr.decode('utf-8'))
