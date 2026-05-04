'''Generates C++ code for simulating outer-totalistic rules.'''
import os
import sys
try:
    from ..genera.hensel import RuleHandler
except:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)) + '/genera')
    from hensel import RuleHandler
rh = RuleHandler()
def gencode():
    '''Generates the code containing high-level functions.'''
    return '''//High-level functions for manipulating patterns.
#include <iostream>
#include "advance.h"
#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
//The below extern statement is required to load a shared library as a CDLL with ctypes.
extern "C" {
using namespace std;
int32_t* cppadvance(int32_t size, int32_t* newsize, const int32_t generations, int32_t lifearray[]) {
    // Internal function used for advancing patterns (for other C++ functions).
	int32_t* newarray = (int32_t*)malloc(size * sizeof(int32_t));
	int32_t* array = newarray;
	int i;
    for (i = 0; i < size; i++) {
        newarray[i] = lifearray[i];
    }
    int32_t newsize2;
	for (i = 0; i < generations; i++) {
		array = advanceone(newarray, size, &newsize2);
		free(newarray);
		newarray = array;
		size = newsize2;
	}
    *newsize = size;
    return newarray;
}
void pyadvance(int32_t size, const int32_t generations, int32_t lifearray[]) {
    // Wrapper function for cppadvance() which saves to a file.
	int32_t* array = (int32_t*)malloc(size * sizeof(int32_t));
    int32_t newsize;
    int32_t* newarray = cppadvance(size, &newsize, generations, lifearray);
    int i;
    string outstring = "{";
	for (i = 0; i < (newsize/2); i++) {
		outstring += "(" + to_string(newarray[2*i]) + "," + to_string(newarray[2*i+1]) + "):1,";
	}
    outstring = outstring + "}";
    FILE* outfile;
    outfile = fopen("outfile.txt", "w");
    fprintf(outfile, outstring.c_str());
    fclose(outfile);
}
}'''
def genadvheader(rule):
    '''Generates the header used to advance patterns.'''
    rule = rh.canoniserule(rule)
    cset = rh.makeconditionset(rule)
    array = []
    for x in range(512):
        if x in cset:
            array.append(1)
        else:
            array.append(0)
    array = str(array).replace('[', '{').replace(']', '}')
    code = '''// Automatically generated C++ header for simulating '''+rule+'''
#include <cstdint>
#include <algorithm>
#include <vector>
#include <unordered_map>
int64_t tokey(const int32_t x, const int32_t y) {
    // Converts an x and y coordinate to a 64-bit key.
	int64_t key;
	key = 2147483648 * (x + 1073741824) + y + 1073741824;
	return key;
}
int32_t getx(const int64_t key) {
    // Extracts the x coordinate from a 64-bit key.
	int32_t x;
	x = key >> 31;
	x -= 1073741824;
	return x;
}
int32_t gety(const int64_t key) {
    // Extracts the y coordinate from a 64-bit key.
	int32_t y;
	y = key % 2147483648;
	y -= 1073741824;
	return y;
}
using namespace std;
// Used for the actual simulation logic.
// The boolean array's contents will depend upon the rule being simulated.
const bool conditionset[512];
// Saves time calculating exponents later:
const int16_t neighbournum[9] = {1, 2, 4, 8, 16, 32, 64, 128, 256};
int32_t* advanceone(const int32_t lifearray[], const uint32_t length, int32_t* outlength) {
    // Advances an array of coordinates by one generation, returning a pointer to the new array.
	int i;
    int64_t key;
    //An unordered map is the best container for the job here.
    //However, the third party robin_hood::unordered_map is much faster.
	unordered_map<int64_t, int> neighbours = {};
	neighbours.reserve(9 * (length / 2));
	int32_t x, y;
    int8_t dx, dy;
    // Calculating neighbours:
	for (i = 0; i < (length / 2); i++) {
        x = lifearray[2*i];
        y = lifearray[2*i+1];
		for (dx = 0; dx < 3; dx++) {
			for (dy = 0; dy < 3; dy++) {
				neighbours[tokey(x + dx - 1, y + dy - 1)] += neighbournum[3*dy + dx];
			}
		}
	}
	int16_t numneighbours;
    int32_t newarraypos = 0;
    // A std::vector is temporarily used to store the new live cells.
	vector<int32_t> newarray;
    newarray.reserve(neighbours.size() * 2);
	for (auto i : neighbours) {
		key = i.first;
		numneighbours = i.second;
        if (conditionset[numneighbours]) {
			newarray.push_back(getx(key));
			newarray.push_back(gety(key));
			newarraypos += 2;
        }
	}
    // Copying them over to a new array:
	int32_t* newarray2 = (int32_t*)malloc(newarraypos * sizeof(int32_t));
	for (i = 0; i < newarraypos; i++) {
		newarray2[i] = newarray[i];
	}
	*outlength = newarraypos;
	return newarray2;
}'''
    code = code.replace('bool conditionset[512];', 'bool conditionset[512] = ' + array+';') 
    if os.path.isfile(os.path.dirname(__file__) + '/includes/robin_hood.h'):
        code = code.replace('<unordered_map>', '\"includes/robin_hood.h\"')
        code = code.replace('unordered_map', 'robin_hood::unordered_map')
    return code
#For testing purposes:
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        rule = sys.argv[1]
    else:
        rule = 'b3s23'
    with open(os.path.dirname(__file__)+'/advance.h', 'w', encoding='utf-8') as f:
        f.write(genadvheader(rule))
    with open(os.path.dirname(__file__)+'/life.cpp', 'w', encoding='utf-8') as f:
        f.write(gencode())
