//Automatically generated C++ code for simulating b3s23.
#include <iostream>
#include "includes/robin_hood.h"
#include <algorithm>
#include <stdint.h>
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
	robin_hood::unordered_map<int64_t, int> neighbours = {};
	robin_hood::unordered_map<int64_t, int> states = {};
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
			if ((numneighbours == -1) or (numneighbours == 2) or(numneighbours == 3)) {
				newarray.push_back(xpos);
				newarray.push_back(ypos);
				newarraypos = newarraypos + 2;
			}
		}
		else {
			if ((numneighbours == -1) or (numneighbours == 3)) {
				newarray.push_back(xpos);
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
}
int main() {
	int size;
	scanf("%d", &size);
	int generations;
	scanf("%d", &generations);
	int32_t* newarray = (int*)malloc(size * sizeof(int32_t));
	int32_t* array = newarray;
	int i;
	int newsize;
	for (i = 0; i < size; i++) {
		scanf("%d", &newarray[i]);
	}
	for (i = 0; i < generations; i++) {
		array = advanceone(newarray, size, &newsize);
		free(newarray);
		newarray = array;
		size = newsize;
	}
	for (i = 0; i < size; i++) {
		printf("%d\n", newarray[i]);
	}
}