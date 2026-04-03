#!/bin/bash
./clean.sh
$(which python3) cythlib/cython_setup.py build_ext --inplace
