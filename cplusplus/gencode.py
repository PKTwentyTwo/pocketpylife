'''Generates C++ code for simulating outer-totalistic rules.'''
import os
def genadvheader(rule):
    '''Generates code for advancing given rule.'''
    splitrule = rule.split('s')
    birth = []
    survival = []
    for x in splitrule[0]:
        if x.isnumeric():
            birth.append(x)
    for x in splitrule[1]:
        if x.isnumeric():
            survival.append(x)
    code = '//Automatically generated C++ header for simulating ' + rule + '''.
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <cstdint>
#include <vector>
int64_t tokey(int32_t x, int32_t y) {
	int64_t key;
	key = 2147483648 * (x + 1073741824) + y + 1073741824;
	return key;
}
int32_t getx(int64_t key) {
	int32_t x;
	x = key >> 31;
	x = x - 1073741824;
	return x;
}
int32_t gety(int64_t key) {
	int32_t y;
	y = key % 2147483648;
	y = y - 1073741824;
	return y;
}
using namespace std;
int32_t* advanceone(int lifearray[], int length, int* outlength) {
	vector<int64_t> livecells = {};
    livecells.reserve(length / 2);
	int i;
    int64_t key;
	for (i = 0; i < (length / 2); i++) {
		livecells.push_back(tokey(lifearray[2*i], lifearray[2*i+1]));
	}
	unordered_map<int64_t, int> neighbours = {};
	unordered_map<int64_t, int> states = {};
	neighbours.reserve(8 * (length / 2));
	states.reserve(length / 2);
	int32_t ux, uy, x, y;
	for (i = 0; i < (length / 2); i++) {
                x = lifearray[2*i];
                y = lifearray[2*i+1];
                states[tokey(x, y)] = 1;
		for (ux = x-1; ux < x+2; ux++) {
			for (uy = y-1; uy < y+2; uy++) {
				if (not ((ux == x) and (uy == y))) {
					key = tokey(ux, uy);
					if (neighbours.find(key) == neighbours.end()) {
						neighbours[key] = 0;
					}
					if (states.find(key) == states.end()) {
						states[key] = 0;
					}
					neighbours[key]++;
				}
			}
		}
	}
	int numneighbours, newarraypos, xpos, ypos;
    	int64_t newkey;
	newarraypos = 0;
	vector<int32_t> newarray = {};
	for (auto i : neighbours) {
		newkey = i.first;
		numneighbours = neighbours[newkey];
		xpos = getx(newkey);
		ypos = gety(newkey);
		if (states[newkey] == 1) {
			if ((numneighbours == -1) or '''
    for x in survival:
        code += '(numneighbours == '+x+') or'
    code = code[:-3] + ') {\n'
    code += '''				newarray.push_back(xpos);
				newarray.push_back(ypos);
				newarraypos = newarraypos + 2;
			}
		}
		else {
			if ((numneighbours == -1) or '''
    for x in birth:
        code += '(numneighbours == '+x+') or'
    code = code[:-3] + ''') {\n				newarray.push_back(xpos);
				newarray.push_back(ypos);
				newarraypos = newarraypos + 2;
			}
		}
	}
	int i2;
	int32_t* newarray2 = (int32_t*)malloc(newarraypos * sizeof(int32_t) + sizeof(int32_t));
	for (i2 = 0; i2 < newarraypos; i2++) {
		newarray2[i2] = newarray[i2];
	}
	*outlength = newarraypos;
	return newarray2;
}'''
    #A faster, third party header file is included:
    if os.path.isfile(os.path.dirname(__file__) + '/includes/robin_hood.h'):
        code = code.replace('<unordered_map>', '\"includes/robin_hood.h\"')
        code = code.replace('unordered_map', 'robin_hood::unordered_map')
    return code
def gencode():
    '''Generates the code containing high-level functions.'''
    return '''//High-level functions for manipulating patterns.
#include <iostream>
#include "advance.h"
#include <algorithm>
#include <cstdint>
#include <vector>
#include <string>
#include <fstream>
//The below extern statement is required to load a shared library as a CDLL with ctypes.
extern "C" {
using namespace std;
int32_t* cppadvance(int32_t size, int32_t* newsize, int32_t generations, int32_t lifearray[]) {
    //Internal function used for advancing patterns (for other C++ functions).
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
void pyadvance(int32_t size, int32_t generations, int32_t lifearray[]) {
    //Wrapper function for cppadvance() which saves to a file.
	int32_t* array = (int32_t*)malloc(size * sizeof(int32_t));
    int32_t newsize;
    int32_t* newarray = cppadvance(size, &newsize, generations, lifearray);
    int i;
    string outstring = "{";
	for (i = 0; i < (newsize/2); i++) {
		outstring = outstring + "(" + to_string(newarray[2*i]) + "," + to_string(newarray[2*i+1]) + "):1,";
	}
    outstring = outstring + "}";
    ofstream outfile("outfile.txt");
    outfile << outstring;
}
}'''
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
