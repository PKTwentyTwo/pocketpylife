# pocketpylife
A Python package for manipulation of patterns in cellular automata.
## Introduction
This is my first Python package, and it contains functions for manipulating patterns in cellular automata.
It was inspired by the much faster [lifelib](https://gitlab.com/apgoucher/lifelib) by Adam P. Goucher, but unlike lifelib, this package:
* Is written entirely in Python (but Cython can be used to improve speed).
* Works regardless of OS and CPU architecture.
It is very slow, however, and so it is mostly written as a test.
## Classes
Cellular automata functionality is implemented through the class ```Lifetree```. A Lifetree is responsible for the actual simulation, using an extremely basic algorithm and an unbounded grid. It does this as a backend to the class ```Pattern```, which stores a dictionary of live cells.
The syntax is very similar to lifelib, with patterns being advanced using ```pt[gens]```, and many functions and properties are similar as well.
## Documentation
Documentation on how to use the rule can be found in the [full documentation](doc/full_documentation.md).
Documentation on the structure of the module can be found [here](doc/structure.md).
## Speed
Given the terrible performance of the library, there are options avaliable to improve speed.

If Cython is avaliable as a module, the function ```cython_compile()``` can be used to compile a shared object to improve the module's performance.
The module attempts to load a shared object first, then loads the Python code if that fails. Remove faulty installations with ```remove_cython_compilation()```.

If g++ (and Cygwin, if running on Windows) is avaliable, then you can call ```pocketpylife.cpplifetree``` to use a ```Lifetree``` that uses C++ code for simulation.
The C++ code is generated automatically at compilation time, but only outer-totalistic rules are supported.

Using Lidka as a benchmark on my (fairly fast) computer, the timings were:
- Pure Python: 122.289 seconds
- Cython:      81.441 seconds
- C++:         34.246 seconds
