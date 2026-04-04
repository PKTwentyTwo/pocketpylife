#!/bin/bash
rm -f cythlib/*.so cythlib/*.c | true
$(which python3) cythlib/cython_setup.py build_ext --inplace
