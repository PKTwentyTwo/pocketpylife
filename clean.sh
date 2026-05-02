#!/bin/bash
#This script is used to clean the repository before committing changes.
#It can also be used to fix any problems that have arisen.
rm -rf cythlib/*.so cythlib/*.c cythlib/*.pyd genera/customrulesim.py cplusplus/*.cpp cplusplus/*.h cplusplus/outfile.txt cythlib/build __pycache__ */__pycache__ cplusplus/bin cplusplus/lib genera/*.rule cplusplus/mingw cplusplus/7za cplusplus/*.zip cplusplus/*.7z | true
python3 cplusplus/gencode.py
dos2unix *.sh __main__.py | true
rm -rf */__pycache__ | true
