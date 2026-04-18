#!/bin/bash
#This script is used to compile Cython shared libraries, as an alternative to calling the Python function.
rm -f cythlib/*.so cythlib/*.c | true
$(which python3) cythlib/cython_setup.py build_ext --inplace
