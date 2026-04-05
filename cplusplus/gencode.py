'''Generates C++ code for simulating outer-totalistic rules.'''
def gencode(rule):
    '''Generates code for a given rule.'''
    splitrule = rule.split('s')
    birth = []
    survival = []
    for x in splitrule[0]:
        if x.isnumeric():
            birth.append(x)
    for x in splitrule[1]:
        if x.isnumeric():
            survival.append(x)
    code = '//Automatically generated C++ code for simulating ' + rule + '''.
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <stdint.h>
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
	int32_t* livecells = (int*)malloc(sizeof(int32_t) * length/2);
	int i, m;
    int64_t key;
	for (i = 0; i < (length / 2); i++) {
		livecells[i] = tokey(lifearray[2*i], lifearray[2*i+1]);
	}
	unordered_map<int64_t, int> neighbours = {};
	unordered_map<int64_t, int> states = {};
	neighbours.reserve(8 * (length / 2));
	states.reserve(length / 2);
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
					neighbours[key]++;
				}
			}
		}
		states[tokey(lifearray[2*i], lifearray[2*i+1])] = 1;
	}
	
	int numneighbours, p, newarraypos, xpos, ypos;
    int64_t newkey;
	newarraypos = 0;
	//Allocate 9x the size of the original list (worst case scenario):
	int32_t* newarray = (int32_t*)malloc(length * 9 * sizeof(int32_t));
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
    code += '''				newarray[newarraypos] = xpos;
				newarray[newarraypos+1] = ypos;
				newarraypos = newarraypos + 2;
			}
		}
		else {
			if ((numneighbours == -1) or '''
    for x in birth:
        code += '(numneighbours == '+x+') or'
    code = code[:-3] + ''') {\n				newarray[newarraypos] = xpos;
				newarray[newarraypos+1] = ypos;
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
	free(newarray);
	//for (i2 = 0; i2 < newarraypos; i2++) {
	//	printf("%d\\n", newarray2[i2]);
	//}
	return newarray2;
}
int main() {
	int size;
	scanf("%d", &size);
	int generations;
	scanf("%d", &generations);
	int32_t* newarray = (int*)malloc(size * sizeof(int));
	int32_t* array = newarray;
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
		printf("%d\\n", newarray[i]);
	}
}'''
    return code
if __name__ == '__main__':
    import os
    with open(os.path.dirname(__file__)+'/life.cpp', 'w', encoding='utf-8') as f:
        f.write(gencode('b3s23'))
