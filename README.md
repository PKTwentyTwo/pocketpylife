# pocketpylife
A Python package for manipulation of patterns in cellular automata.
## Introduction
This is my first Python package, and it contains functions for manipulating patterns in cellular automata.
It was inspired by the much faster [lifelib](https://gitlab.com/apgoucher/lifelib) by Adam P. Goucher, but unlike lifelib, this package:
* Is written entirely in Python (but there are ways to improve speed).
* Works regardless of OS and CPU architecture.
It is very slow, however, and so it is mostly written as a test.
## Classes
Cellular automata functionality is implemented through the class ```Lifetree```. A Lifetree is responsible for the actual simulation, using an extremely basic algorithm and an unbounded grid. It does this as a backend to the class ```Pattern```, which stores a dictionary of live cells.
The syntax is very similar to lifelib, with patterns being advanced using ```pt[gens]```, and many functions and properties are similar as well.
## Documentation
Documentation on how to use the module can be found in the [full documentation](doc/full_documentation.md).
Documentation on the structure of the module can be found [here](doc/structure.md).
## Speed
Given the terrible performance of the library, there are options avaliable to improve speed.

If Cython is avaliable as a module, the function ```cython_compile()``` can be used to compile a shared object to improve the module's performance.
The module attempts to load a shared object first, then loads the Python code if that fails. Remove faulty installations with ```remove_cython_compilation()```.

If g++ (and Cygwin, if running on Windows) is avaliable, then you can call ```pocketpylife.cpplifetree()``` to use a ```Lifetree``` that uses C++ code for simulation.
The C++ code is generated automatically at compilation time, but only outer-totalistic rules are supported.

Using the methuselah [Lidka](https://conwaylife.com/wiki/Lidka) as a benchmark on my (fairly fast) computer with WSL, the timings were:
- Pure Python: 116.192 seconds
- Cython:      78.185 seconds (32.7% reduction in time). Compilation: 12 seconds
- C++:         21.99 seconds (81.1% reduction in time).  Compilation: 0.76 seconds/rule

For Windows using Git Bash, the timings were:
- Pure Python: 116.26 seconds
- Cython: 72.648 seconds (37.5% reduction in time).      Compilation: 8 seconds (using Microsoft's cl.exe).
- C++: 35.98 seconds (69.1% reduction in time).          Compilation: 1.65 seconds/rule (g++ for Cygwin isn't the fastest.)

For a Raspberry Pi 5 running Ubuntu Server, tested over an SSH connection:
- Pure Python: 252.998 seconds 
- Cython: 182.089 seconds (28.0% reduction in time).     Compilation: 23.5 seconds
- C++: 51.828 seconds (79.5% reduction in time).         Compilation: 0.96 seconds/rule

Compare these times with the below for an idea of how slow they are:
- Lifelib: 0.00055 seconds. Compilation: 22 seconds/rule
## License and credits
The module is licensed under the permissive MIT license.
The header file [robin_hood.h](cplusplus/includes/robin_hood.h) is taken from [martinus's robin_hood_hashing](https://github.com/martinus/robin-hood-hashing), which is licensed under a separate MIT license. It is not essential; the C++ code generator will default to ```std::unordered_map``` if no header file is found.
Note that Cygwin, which is used for compilation on Windows, is licensed under the LGPL and uses GPL components, including the g++ compiler. No (L)GPL software is included by default, as the Cygwin installer is downloaded just before it is required.

