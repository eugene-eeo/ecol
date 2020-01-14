/*
 * bitset.c
 * ========
 *
 * Tiny bitset implementation for small bitsets (<= 64).
 *
 */

#include "bitset.h"

const bitset BITSET_INIT = 0;

// Set bit pos to val
bitset bitset_set(bitset bs, int pos, int val) {
    if (!val) {
        return bs & (INT64_MAX ^ ((uint64_t)1 << pos));
    }
    return bs | ((uint64_t)1 << pos);
}

// Intersection of a and b
bitset bitset_intersection(bitset a, bitset b) {
    return a & b;
}

// Union between a and b
bitset bitset_union(bitset a, bitset b) {
    return a | b;
}

// Count the number of bits set
int bitset_count(bitset a) {
    return __builtin_popcountl(a);
}

// Find first set bit
int bitset_first(bitset a) {
    return __builtin_ffsl(a) - 1;
}
