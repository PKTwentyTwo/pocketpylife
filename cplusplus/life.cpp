//High-level functions for manipulating patterns.
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
}