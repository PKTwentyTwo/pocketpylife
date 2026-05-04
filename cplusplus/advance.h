// Automatically generated C++ header for simulating b3s23
#include <cstdint>
#include <algorithm>
#include <vector>
#include "includes/robin_hood.h"
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
const bool conditionset[512] = {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// Saves time calculating exponents later:
const int16_t neighbournum[9] = {1, 2, 4, 8, 16, 32, 64, 128, 256};
int32_t* advanceone(const int32_t lifearray[], const uint32_t length, int32_t* outlength) {
    // Advances an array of coordinates by one generation, returning a pointer to the new array.
	int i;
    int64_t key;
    //An unordered map is the best container for the job here.
    //However, the third party robin_hood::robin_hood::unordered_map is much faster.
	robin_hood::unordered_map<int64_t, int> neighbours = {};
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
}