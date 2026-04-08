#!/bin/bash
#This script is used to clean the repository before committing changes.
#It can also be used to fix any problems that have arisen.
rm -rf cythlib/*.so cythlib/*.c cythlib/*.pyd genera/customrulesim.py cplusplus/*.cpp cythlib/build __pycache__ */__pycache__ cplusplus/bin cplusplus/cygwin cplusplus/cygdirs.txt genera/ruletable.rule | true
python3 cplusplus/cygwin.py
dos2unix *.sh */*.sh __main__.py | true
