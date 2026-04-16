
# Full documentation
This document explains the entire syntax and structure of the library.
## Full list of functions
The complete list of top-level functions is displayed below:
- ```pocketpylife.lifetree(rule)```: Creates a new Lifetree for the given rule. The specified rule can be INT (or any subset), Generations, or the path to a ruletable file.
- ```pocketpylife.cpplifetree(rule, force_compile = False)```: Creates a new Lifetree with C++ simulation for the given rule. Throws an error if g++ is not avaliable, or the rule is not OT.
Windows exclusive functions:
- ```pocketpylife.install_cygwin()```: Installs Cygwin in the [cplusplus](../cplusplus) directory. This is required for compilation of C++ code.
- ```pocketpylife.add_cygdir()```: Adds a directory to [cygdirs.txt](../cplusplus/cygdirs.txt). Useful if you already have a Cygwin installation.
Functions avaliable if Cython is installed:
- ```pocketpylife.cython_compile()```: Compiles the Cython code in the [cythlib](../cythlib) folder, which improves speed by 25-30%.
- ```pocketpylife.remove_cython_compilation()```: Removes any Cython shared libraries. Useful to fix buggy installations.
## How to use lifetrees:
A ```lifetree``` is the Python class used to create and evolve patterns. To create one, simply run:

```lt = pocketpylife.lifetree('b3s23')```
One parameter must be supplied: the rule to be used. This must be specified using [Hensel notation.](https://conwaylife.com/wiki/Isotropic_non-totalistic_rule#Square_grid) 
All isotropic rules excluding B0 are supported, and the default rule (if no rule is given) is B3/S23, the rulestring for the Game of Life. A class ```RuleGenerator``` is used to convert Hensel notation rules into a set of integers from 0-511 at ```lifetree``` creation, and this set is used to evolve patterns.

The main use for a ```lifetree``` is pattern creation; to create a new pattern, use ```lifetree.pattern()```:
```pt = lt.pattern('2o$2o2$4o$o2bo!')```
```pt2 = lt.pattern('xs10_32qr')```
Both the [RLE](https://conwaylife.com/wiki/Run_Length_Encoded) and [apgcode](https://conwaylife.com/wiki/Apgcode) formats are supported, and running ```lifetree.pattern()``` will return a new instance of the ```Pattern``` class.
### Other functions of lifetrees:
Some miscellaneous utility functions are avaliable, including the following:

 ```lifetree.hashsoup()``` generates a ```Pattern``` representing a [soup](https://conwaylife.com/wiki/Soup) based on an SHA-256 hash and a symmetry. 
 Example usage:
 ```soup = lt.hashsoup('test_instring', 'C1')```
 The first argument is a text string to be run through SHA-256, and the second is the symmetry.
 Available symmetries currently include:
 

 - C1 - A 16x16 asymmetric soup.
 - C2_1 - Invariant under 180° rotation around the midpoint of a cell.
 - C2_2 - Invariant under 180° rotation around the edge of two cells.
 - C2_4 - Invariant under 180° rotation around the vertex of four cells.
 - C4_1 - Invariant under 90° rotation around the midpoint of a cell.
 - C4_4 - Invariant under 90° rotation around the vertex of four cells.
 - D2_+1 - Invariant under reflection in a line passing through the midpoints of cells.
 - D2_+2 - Invariant under reflection in a line passing between two cells.
 - D2_x - Invariant under reflection in a diagonal line.
 - D4_+1 - Invariant under reflection in two lines, which meet at the midpoint of a cell.
 - D4_+2 - Invariant under reflection in two lines, which meet at the edge of two cells.
 - D4_+4 - Invariant under reflection in two lines, which meet at the vertex of four cells.
 - D4_x1 - Invariant under reflection in two diagonal lines, which meet at the midpoint of a cell.
 - D4_x4 - Invariant under reflection in two diagonal lines, which meet at the vertex of four cells.
 - D8_1 - Invariant under reflection in four lines, which meet at the midpoint of a cell.
 - D8_4 - Invariant under reflection in four lines, which meet at the vertex of four cells.
 
 Another useful function is ```lifetree.download_soups()```, which downloads soups from [Catagolue](https://catagolue.hatsya.com/home) that produce a specified apgcode, and returns a list of ```Pattern``` objects. 
 The following usage would return a list of asymmetric soups that contain an [Omnibus](https://conwaylife.com/wiki/Omnibus) in their final ash:
 ```soups = lt.download_soups('xs40_gj1u0u1jgzdlgf0fgld', 'C1')```

For lifetrees configured for standard Life, a function exists to download the [glider synthesis](https://conwaylife.com/wiki/Glider_synthesis) of a given apgcode:
```synth = lt.download_synthesis('xs40_gj1u0u1jgzdlgf0fgld')```
## Working with patterns
The class ```Pattern``` is used to represent patterns, and provides a range of functions  for manipulation of them.

A range of read-only properties are available:

 - ```pt.rle```: Returns the RLE of the pattern as a string, including the header.
 - ```pt.population```: Returns the number of live cells in the pattern.]
 - ```pt.coords```: Returns a list of tuples representing the coordinates of every live cell in the pattern.
 - ```pt.firstcell```: Returns a tuple ```(x, y)``` of the first live cell in the pattern.
 - ```pt.digest```: Returns an integer digest of the pattern, which is orientation-dependent. Identical patterns will have the same digest, so it is useful for comparison.
 - ```pt.octodigest```: Returns an integer digest of the pattern. Unlike ```pt.digest```,  the orientation does not matter.
 - ```pt.period```: Returns the period of the pattern. If the pattern is not periodic (determined if it does not stabilise in 1024 generations), it will raise a ```ValueError```.
 - ```pt.displacement```: Returns the period of the pattern as a tuple ```(dx, dy)```.  Again, a ```ValueError``` will be raised if the pattern is not periodic within 1024 generations.
 - ```pt.bbox```: Returns the bounding box of the pattern as a tuple ```(x, y, dy, dx)```. If the pattern is empty, it will instead return ```None```.
 - ```pt.components```: Returns a list of ```Pattern``` objects representing the connected 'islands' in the pattern
 - ```pattern.apgcode```: Returns the apgcode of the pattern. If it is aperiodic, it will return the string ```"aperiodic"```.
 
 Pattern manipulation can be done using the syntax below:
 
 - ```Pattern[gens]``` evolves the pattern by the specified number of generations.
 - ```Pattern(dx, dy)``` translates the pattern by ```(dx, dy)```.
 - ```Pattern(transformation)``` applies the given transformation to the pattern. Currently supported transformations are ```identity```, ```flip_x```, ```flip_y```, ```rot_90```, ```rot_180```, ```rot_270```, ```flip_xy```, ```rcw```, and ```rccw```.
 Patterns can also be manipulated using each other:
 
 - ```pt1 + pt2``` returns the union of two patterns - cells that are alive in either will be alive in the resultant pattern.
 - ```pt1 - pt2``` returns the difference of two patterns - only cells that are alive in ```pt1``` and dead in ```pt2``` will be alive in the resultant pattern.
 - ```pt1 ^ pt2``` returns the symmetric difference of two patterns - only cells that are alive in exactly one pattern will be alive in the resultant pattern,


