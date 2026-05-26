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
using namespace std;
void cppadvance(vector<pair<int32_t, int32_t> >& lifevector, const int32_t generations) {
    // Internal function used for advancing patterns (for other C++ functions).
    int32_t i;
    for (i = 0; i < generations; i++) {
        advanceone(lifevector);
    }
}
extern "C" {
void pyadvance(const int32_t size, const int32_t generations, const int32_t lifearray[], const int32_t filenum) {
    // Wrapper function for cppadvance() which saves to a file.
    int32_t newsize;
    vector<pair<int32_t, int32_t> > lifevector;
    pair<int32_t, int32_t> cpair;
    int32_t i;
    for (i = 0; i < size/2; i++) {
        cpair = make_pair(lifearray[2*i], lifearray[2*i+1]);
        lifevector.push_back(cpair);
    }
    cppadvance(lifevector, generations);
    string outstring = "{";
    for (i = 0; i < (lifevector.size()); i++) {
        cpair = lifevector[i];
        outstring += "(" + to_string(cpair.first) + "," + to_string(cpair.second) + "):1,";
    }
    outstring = outstring + "}";
    string filename = "outfile" + to_string(filenum) + ".txt";
    ofstream outfile(filename);
    outfile << outstring;
    outfile.close();
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
    code = '''// Automatically generated C++ header for simulating b3s23
#include <cstdint>
#include <algorithm>
#include <vector>
#include <utility>
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
#define MAXINC 9
void advanceone(vector<pair<int32_t, int32_t> >& lifevector) {
    // Advances an array of coordinates by one generation, returning a pointer to the new array.
    int i;
    int64_t key;
    //An unordered map is the best container for the job here.
    //However, the third party ankerl::unordered_dense::map is much faster.
    unordered_map<int64_t, uint16_t> neighbours = {};
    neighbours.reserve(MAXINC * lifevector.size());
    int32_t x, y;
    uint8_t dx, dy;
    pair<int32_t, int32_t> cpair;
    // Calculating neighbours:
    for (i = 0; i < (lifevector.size()); i++) {
        auto [x, y] = lifevector[i];
        for (dx = 0; dx < 3; dx++) {
            for (dy = 0; dy < 3; dy++) {
                neighbours[tokey(x + dx - 1, y + dy - 1)] += neighbournum[3*dy + dx];
            }
        }
    }
    uint16_t numneighbours;
    // A std::vector is temporarily used to store the new live cells.
    lifevector.clear();
    lifevector.reserve(neighbours.size());
    for (const auto& kv : neighbours) {
        if (conditionset[kv.second]) {
            key = kv.first;
            lifevector.push_back(make_pair(getx(key), gety(key)));
        }
    }
}'''
    code = code.replace('bool conditionset[512];', 'bool conditionset[512] = ' + array+';') 
    if os.path.isfile(os.path.dirname(__file__) + '/includes/unordered_dense.h'):
        code = code.replace('<unordered_map>', '\"includes/unordered_dense.h\"')
        code = code.replace('unordered_map', 'ankerl::unordered_dense::map')
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
