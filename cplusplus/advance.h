// Automatically generated C++ header for simulating b3s23
#include <cstdint>
#include <algorithm>
#include <vector>
#include <utility>
#include "includes/unordered_dense.h"
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
#define MAXINC 9
void advanceone(vector<pair<int32_t, int32_t> >& lifevector) {
    // Advances an array of coordinates by one generation, returning a pointer to the new array.
    int i;
    int64_t key;
    //An unordered map is the best container for the job here.
    //However, the third party ankerl::unordered_dense::map is much faster.
    ankerl::unordered_dense::map<int64_t, uint16_t> neighbours = {};
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
}