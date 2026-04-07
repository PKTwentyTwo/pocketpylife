'''Responsible for dealing with C++ compilation.'''
import os
import struct
import subprocess
import sys
import time
try:
    from ..genera.hensel import RuleHandler
    from ..genera.findgenera import getgenera
    from .gencode import gencode
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/genera')
    from hensel import RuleHandler
    from findgenera import getgenera
    from gencode import gencode
if os.name == 'nt':
    try:
        from .cygwin import getcygdir, copydlls
    except ImportError:
        from cygwin import getcygdir, copydlls
rh = RuleHandler()
cppdir = os.path.dirname(__file__)
def get_bash():
    '''Returns what bash is going to be used for compilation.'''
    #Bash is needed to run the g++ compiler, and it is installed by default on POSIX systems.
    #Windows doesn't have it by default, but Cygwin provides a sufficient alternative.
    if os.name == 'posix':
        return ['/bin/bash', cppdir + '/cygbash.sh']
    else:
        return [getcygdir() + '/bin/bash.exe', cppdir + '/cygbash.sh']
def dos2unix(file):
    '''Converts a file from DOS format to Unix format.
Needed to fix the fact that Git Bash is stupid and automatically does the opposite.'''
    with open(file, 'rb') as f:
        content = f.read()
    content = content.replace(b'\n\r', b'\n')
    with open(file, 'wb') as f:
        f.write(content)
def getcompiler():
    '''Determines if it is feasible to compile in the current working environment.
Throws an error if compilation is not possible, and otherwise returns the compiler.'''
    #Check if the architecture is 64-bit:
    numbits = 8 * struct.calcsize("P")
    if numbits != 64:
        raise OSError('C++ bindings are currently not avaliable for '+str(numbits)+'-bit systems.')
    #Check that g++ is avaliable:
    dos2unix(cppdir + '/cygbash.sh')
    try:
        gpp_location = subprocess.check_output(get_bash() + ['which', 'g++']).decode('utf-8').replace('\n', '')
    except subprocess.CalledProcessError:
        raise OSError('''g++ does not appear to be installed on this system.
Try installing it with: sudo apt install g++''')
    return 'g++'
def isvalid(rule):
    '''Determines whether a rule is valid or not for code generation.'''
    genera = getgenera(rule)
    return genera in ['b3s23life', 'lifelike']
def compilerule(rule,
                compilerargs = ['-O3', '-march=native', '-funroll-loops']):
    '''Generates and compiles code for a given rule.'''
    if not isvalid(rule):
        raise ValueError('Rule '+rule+' belongs to genus \''+getgenera(rule)+'\' and cannot be compiled.')
    rule = rh.canoniserule(rule)
    if not os.path.exists(cppdir+'/bin'):
        os.mkdir(cppdir+'/bin')
    #Generate the code:
    code = gencode(rule)
    with open(cppdir + '/life.cpp', 'w', encoding = 'utf-8') as f:
        f.write(code)
    dos2unix(cppdir + '/cygbash.sh')
    #Write a command to compile the code:
    command = get_bash() + [getcompiler()]
    command += [cppdir+'/life.cpp', '-o', cppdir+'/bin/'+rule]
    command += compilerargs
    joinedcommand = ''
    for x in command:
        joinedcommand += x + ' '
    joinedcommand = joinedcommand[:-1]
    sys.stderr.write('Attempting compilation with command:\n'+joinedcommand+'\n')
    starttime = time.time()
    #Compile the code:
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compiler_stdout, compiler_stderr = proc.communicate()
    status = proc.returncode
    if os.name == 'nt':
        copydlls()
    if status == 0:
        sys.stderr.write('Compilation succeeded in '+str(round(time.time() - starttime, 3))+' seconds.\n')
        os.remove(cppdir+'/life.cpp')
    else:
        raise ValueError('Error occurred during compilation!\n\n' + compiler_stderr.decode('utf-8'))
