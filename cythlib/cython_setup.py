'''Used to compile a .so or .pyd to improve speed.'''
import os
import platform
import sys
import time
from setuptools import setup, Extension
from Cython.Build import cythonize
def cython_compile(force_recompile = True):
    '''Compiles a Cython library to improve speed.
Requires that Cython is installed as a Python package.'''
    if (not force_recompile) and extensions_exist():
        return None
    executable = sys.executable
    executable = os.path.basename(executable)
    if executable.endswith('.exe'):
        executable = executable[:-4]
    cmd = executable + ' \"' + __file__ + '\" build_ext --inplace'
    sys.stderr.write('Attempting to compile using following command:\n')
    sys.stderr.write(cmd + '\n')
    os.system(cmd)
def remove_cython_compilation():
    '''Deletes any compiled Cython libraries.'''
    dirloc = os.path.dirname(__file__)
    locfiles = os.listdir(dirloc)
    locfiles = [x for x in locfiles if x.endswith('.so') or x.endswith('.pyd')]
    total = 0
    for n in locfiles:
        total += 1
        os.remove(dirloc + '/' + n)
    sys.stderr.write('Successfully removed '+str(total)+' files.')
def extensions_exist():
    '''Determines if Cython extensions have been compiled or not.'''
    cythdir = os.path.dirname(__file__)
    files = [x for x in os.listdir(cythdir) if x.endswith('.so') or x.endswith('.pyd')]
    files = [x[0:x.find('.')] for x in files]
    return 'cygridops' in files and 'cylifetree' in files
if __name__ == '__main__':
    starttime = time.time()
    #Delete any  old files:
    oldcwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    files = os.listdir(os.getcwd())
    files = [x for x in files if x.endswith('.so') or x.endswith('.pyd')]
    for x in files:
        os.remove(x)
    #Create a .pyx file:
    compilerargs = ["-O3", "-march=native", "-ffast-math"]
    if platform.uname()[0] == 'Windows':
        compilerargs = ['/O2']
    extensions = [
        Extension(
            name="cylifetree",
            sources=["cylifetree.pyx"],
            language="c",
            extra_compile_args=compilerargs,
        )
    ]

    setup(
        name="cylifetree",
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                "language_level": "3",
                "boundscheck": False,
                "wraparound": True,
                "cdivision": True
            }
        ),
    )
    #Rename the output file:
    files = os.listdir(os.getcwd())
    files = [x for x in files if (x.endswith('.so') or x.endswith('.pyd')) and x.startswith('cylifetree')]
    if len(files) == 0:
        raise FileNotFoundError('Could not locate compiled .so or .pyd!')
    file = files[0]
    if file.endswith('.so'):
        EXTENSION = '.so'
    else:
        EXTENSION = '.pyd'
    with open(file, 'rb') as f:
        code = f.read()
    with open('cylifetree' + EXTENSION, 'wb') as f:
        f.write(code)
    os.remove(file)
    #Next, compile the gridops file:
    compilerargs = ["-O3", "-march=native", "-ffast-math"]
    if platform.uname()[0] == 'Windows':
        compilerargs = ['/O2']
    extensions = [
        Extension(
            name="cygridops",
            sources=["cygridops.pyx"],
            language="c",
            extra_compile_args=compilerargs,
        )
    ]

    setup(
        name="cygridops",
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                "language_level": "3",
                "boundscheck": False,
                "wraparound": False,
                "cdivision": True
            }
        ),
    )
    #Rename the output file:
    files = os.listdir(os.getcwd())
    files = [x for x in files if (x.endswith('.so') or x.endswith('.pyd')) and x.startswith('cygridops')]
    if len(files) == 0:
        raise FileNotFoundError('Could not locate compiled .so or .pyd!')
    file = files[0]
    if file.endswith('.so'):
        EXTENSION = '.so'
    else:
        EXTENSION = '.pyd'
    with open(file, 'rb') as f:
        code = f.read()
    with open('cygridops' + EXTENSION, 'wb') as f:
        f.write(code)
    os.remove(file)
    #Clean up the C files:
    if os.path.isfile('cylifetree.c'):
        os.remove('cylifetree.c')
    if os.path.isfile('cygridops.c'):
        os.remove('cygridops.c')
    os.chdir(oldcwd)
    sys.stderr.write('Compilation succeeded in '+str(round(time.time() - starttime, 3))+' seconds.\n')
