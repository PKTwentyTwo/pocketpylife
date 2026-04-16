'''Contains functions for dealing with Cygwin on Windows.'''
import os
import shutil
import subprocess
from urllib.request import urlretrieve
cppdir = os.path.dirname(__file__)
rootdir = os.path.dirname(cppdir)
#Get the list of directories containing Cygwin.
cygdir_file = cppdir + '/cygdirs.txt'
if not os.path.isfile(cygdir_file):
    with open(cygdir_file, 'w', encoding='utf-8') as f:
        f.write('#This file stores directories containing Cygwin.\n')
cygdirs = []
with open(cygdir_file, 'r', encoding='utf-8') as f:
    cygdirs = f.read().split('\n')
def getcygdir():
    '''Returns the first directory found that contains Cygwin.'''
    cygdirs.append(cppdir + '/cygwin')
    #Check each directory to see if it is valid:
    for x in cygdirs:
        if x.startswith('#'):
            #This allows for comments to be added.
            continue
        if os.path.isdir(x) and os.path.isfile(x + '/bin/bash.exe'):
            return os.path.abspath(x)
    raise ValueError('''Unable to locate a valid Cygwin directory!
Try running pocketpylife.install_cygwin(),
or add an installation using pocketpylife.add_cygdir().''')
def add_cygdir(directory):
    '''Adds a directory containing Cygwin to the module's list of potential directories.'''
    cygdirs.append(directory)
    text = ''
    for x in cygdirs:
        if (os.path.isdir(x) and os.path.isfile(x + '/bin/bash.exe')) or x.count('#') > 0:
            if x.count('#') == 0:
                text += '\n' + os.path.abspath(x) + '\n'
            else:
                text += x + '\n'
    with open(cygdir_file, 'w', encoding='utf-8') as f:
        f.write(text)
def install_cygwin(root = None, packages = ['gcc-g++']):
    '''Installs Cygwin with the specified packages.'''
    #This function only ever needs to be called on Windows:
    if os.name != 'nt':
        print('Skipping installation as Cygwin is only required on Windows.')
        return
    #Need to set up some file paths:
    packdir = cppdir + '/cygwin/packages'
    setup_executable = cppdir + '/cygwin/setup-x86_64.exe'
    if root is None:
        root = cppdir + '/cygwin/cygwin64'
    root = os.path.abspath(root)
    packdir = os.path.abspath(packdir)
    setup_executable = os.path.abspath(setup_executable)
    if not os.path.exists(packdir):
        os.makedirs(packdir)
    if os.path.exists(setup_executable):
        os.remove(setup_executable)
    print('Downloading setup executable...')
    urlretrieve('https://cygwin.com/setup-x86_64.exe', setup_executable)
    command = [setup_executable, '--no-admin',
               '-q', '-n', '-N', '-d',
               '-R', root,
               '-l', packdir,
               '-s', 'http://mirrors.kernel.org/sourceware/cygwin',
               '-P', ','.join(packages)]
    print('Attempting installation...')
    subprocess.check_call(command)
    print('Installation complete.')
    add_cygdir(root)
def copydlls():
    '''Copies the necessary DLLs across to the folder containing compiled rule binaries.'''
    dlls = ['cygstdc++-6.dll',
        'cygwin1.dll',
        'cyggcc_s-seh-1.dll',
        'cygiconv-2.dll',
        'cygintl-8.dll']
    for x in dlls:
        if os.path.isfile(cppdir + '/bin/' + x):
            os.remove(cppdir + '/bin/' + x)
        shutil.copy(getcygdir() + '/bin/' + x, cppdir + '/bin')
