//High-level functions for manipulating patterns.
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
}