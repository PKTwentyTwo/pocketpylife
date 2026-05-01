'''Responsible for dealing with C++ compilation.'''
import os
import struct
import subprocess
import sys
import time
try:
    from ..genera.hensel import RuleHandler
    from ..genera.findgenera import getgenera
    from .gencode import gencode, genadvheader
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/genera')
    from hensel import RuleHandler
    from findgenera import getgenera
    from gencode import gencode, genadvheader
if os.name == 'nt':
    try:
        from .mingw import get_mingw_compiler
    except ImportError:
        from mingw import get_mingw_compiler
rh = RuleHandler()
cppdir = os.path.dirname(__file__)
def getcompiler():
    '''Determines if it is feasible to compile in the current working environment.
Throws an error if compilation is not possible, and otherwise returns the compiler.'''
    #Check if the architecture is 64-bit:
    numbits = 8 * struct.calcsize("P")
    if numbits != 64:
        raise OSError('C++ bindings are currently not avaliable for '+str(numbits)+'-bit systems.')
    #Use mingw64 on Windows:
    if os.name == 'nt':
        return get_mingw_compiler()
    #Check that g++ is avaliable:
    try:
        subprocess.check_output(['/bin/bash', 'which', 'g++']).decode('utf-8').replace('\n', '')
    except subprocess.CalledProcessError:
        raise OSError('''g++ does not appear to be installed on this system.
Try installing it with: sudo apt install g++''')
    return 'g++'
def isvalid(rule):
    '''Determines whether a rule is valid or not for code generation.'''
    genera = getgenera(rule)
    return genera in ['b3s23life', 'lifelike']
def compilerule(rule,
                compilerargs = ['-O3',
                                '-march=native',
                                '-flto']):
    '''Generates and compiles code for a given rule.'''
    if not isvalid(rule):
        raise ValueError('Rule '+rule+' belongs to genus \''+getgenera(rule)+'\' and cannot be compiled.')
    rule = rh.canoniserule(rule)
    if not os.path.exists(cppdir+'/bin'):
        os.mkdir(cppdir+'/bin')
    #Generate the code:
    code = genadvheader(rule)
    with open(cppdir + '/advance.h', 'w', encoding = 'utf-8') as f:
        f.write(code)
    code = gencode()
    with open(cppdir + '/life.cpp', 'w', encoding = 'utf-8') as f:
        f.write(code)
    #Write a command to compile the code:
    command = [getcompiler()]
    command += [cppdir+'/life.cpp', '-o', cppdir+'/bin/'+rule+'.so', '-shared', '-fPIC']
    command += compilerargs
    if os.name == 'nt':
        #Required to avoid DLL hell:
        #https://en.wikipedia.org/wiki/DLL_hell
        command += ['-static', '-static-libgcc', '-static-libstdc++']
    joinedcommand = ''
    for x in command:
        joinedcommand += x + ' '
    joinedcommand = joinedcommand[:-1]
    sys.stderr.write('Attempting compilation with command:\n'+joinedcommand+'\n')
    starttime = time.time()
    if os.path == 'nt':
        wd = os.path.dirname(getcompiler())
    else:
        wd = os.getcwd()
    cwd = os.getcwd()
    #Compile the code:
    os.chdir(wd)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=wd)
    os.chdir(cwd)
    compiler_stdout, compiler_stderr = proc.communicate()
    status = proc.returncode
    if status == 0:
        sys.stderr.write('Compilation succeeded in '+str(round(time.time() - starttime, 3))+' seconds.\n')
    else:
        raise ValueError('Error occurred during compilation!\n\n' + compiler_stderr.decode('utf-8'))
if __name__ == '__main__':
    if len(sys.argv) == 1:
        compilerule('b3s23')
    else:
        compilerule(sys.argv[1])
