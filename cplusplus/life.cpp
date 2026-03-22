//A C++ implementation for simulating B3/S23.
#include <iostream>
#include <unordered_map>
#include <stdlib.h>
#include <algorithm>
int tokey(int x, int y) {
	int key;
	key = 32768 * (x + 16384) + y + 16384;
	return key;
}
int getx(int key) {
	int x;
	x = key / 32768;
	x = x - 16384;
	return x;
}
int gety(int key) {
	int y;
	y = key % 32768;
	y = y - 16384;
	return y;
}
using namespace std;
int* advanceone(int lifearray[], int length, int* outlength) {
	int* livecells = (int*)malloc(sizeof(int) * length/2);
	int i, m, key;
	for (i = 0; i < (length / 2); i++) {
		livecells[i] = tokey(lifearray[2*i], lifearray[2*i+1]);
	}
	unordered_map<int, int> neighbours = {};
	unordered_map<int, int> states = {};
	int dx, dy;
	for (i = 0; i < (length / 2); i++) {
		for (dx = -1; dx < 2; dx++) {
			for (dy = -1; dy < 2; dy++) {
				if (not ((dx == 0) and (dy == 0))) {
					key = tokey(lifearray[2*i] + dx, lifearray[2*i+1]+dy);
					if (neighbours.find(key) == neighbours.end()) {
						neighbours[key] = 0;
					}
					if (states.find(key) == states.end()) {
						states[key] = 0;
					}
					neighbours[key] = neighbours[key] + 1;
				}
			}
		}
		states[tokey(lifearray[2*i], lifearray[2*i+1])] = 1;
	}
	
	int newkey, numneighbours, p, newarraypos, xpos, ypos;
	newarraypos = 0;
	//Allocate 9x the size of the original list (worst case scenario):
	int* newarray = (int*)malloc(length * 9 * sizeof(int));
	for (auto i : neighbours) {
		newkey = i.first;
		numneighbours = neighbours[newkey];
		xpos = getx(newkey);
		ypos = gety(newkey);
		if (states[newkey] == 1) {
			if ((numneighbours == 2) or (numneighbours == 3)) {
				newarray[newarraypos] = xpos;
				newarray[newarraypos+1] = ypos;
				newarraypos = newarraypos + 2;
			}
		}
		else {
			if (numneighbours == 3) {
				newarray[newarraypos] = xpos;
				newarray[newarraypos+1] = ypos;
				newarraypos = newarraypos + 2;
			}
		}
	}
	int i2;
	int* newarray2 = (int*)malloc(newarraypos * sizeof(int) + sizeof(int));
	for (i2 = 0; i2 < newarraypos; i2++) {
		newarray2[i2] = newarray[i2];
	}
	*outlength = newarraypos;
	free(newarray);
	//for (i2 = 0; i2 < newarraypos; i2++) {
	//	printf("%d\n", newarray2[i2]);
	//}
	return newarray2;
}
int main() {
	int size;
	scanf("%d", &size);
	int generations;
	scanf("%d", &generations);
	int* newarray = (int*)malloc(size * sizeof(int));
	int* array = newarray;
	int i, j;
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