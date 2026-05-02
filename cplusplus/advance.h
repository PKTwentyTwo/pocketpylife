//Automatically generated C++ header for simulating b3s23
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <vector>
#include "includes/robin_hood.h"
int64_t tokey(const int32_t x, const int32_t y) {
	int64_t key;
	key = 2147483648 * (x + 1073741824) + y + 1073741824;
	return key;
}
int32_t getx(const int64_t key) {
	int32_t x;
	x = key >> 31;
	x = x - 1073741824;
	return x;
}
int32_t gety(const int64_t key) {
	int32_t y;
	y = key % 2147483648;
	y = y - 1073741824;
	return y;
}
using namespace std;
const int conditionset[512] = {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
const int neighbournum[9] = {1, 2, 4, 8, 16, 32, 64, 128, 256};
int32_t* advanceone(const int32_t lifearray[], const int length, int32_t* outlength) {
	int i;
    int64_t key;
	robin_hood::unordered_map<int64_t, int> neighbours = {};
	neighbours.reserve(9 * (length / 2));
	int32_t dx, dy, x, y;
	for (i = 0; i < (length / 2); i++) {
        x = lifearray[2*i];
        y = lifearray[2*i+1];
		for (dx = 0; dx < 3; dx++) {
			for (dy = 0; dy < 3; dy++) {
				key = tokey(x + dx - 1, y + dy - 1);
				neighbours[key] = neighbours[key] + neighbournum[3*dy + dx];
			}
		}
	}
	int numneighbours;
    int32_t newarraypos = 0;
    int64_t newkey;
	vector<int32_t> newarray = {};
    newarray.reserve(neighbours.size() * 2);
	for (auto i : neighbours) {
		newkey = i.first;
		numneighbours = neighbours[newkey];
        if (conditionset[numneighbours]) {
			newarray.push_back(getx(newkey));
			newarray.push_back(gety(newkey));
			newarraypos = newarraypos + 2;
        }
	}
	int32_t* newarray2 = (int32_t*)malloc(newarraypos * sizeof(int32_t));
	for (i = 0; i < newarraypos; i++) {
		newarray2[i] = newarray[i];
	}
	*outlength = newarraypos;
	return newarray2;
}