/*
 * bitset.c
 * ========
 *
 * Tiny bitset implementation for small bitsets (<= 64).
 * Needs -mbmi2 when compiling.
 *
 */

#include "bitset.h"
#include <x86intrin.h>

const bitset BITSET_INIT = 0;

// Set bit pos to val
bitset bitset_set(bitset bs, int pos, int val) {
    int64_t mask = (((uint64_t)1) << pos);
    if (val) {
        return bs | mask;
    } else {
        return bs & ~mask;
    }
}

// Test bit
int bitset_test(bitset bs, int pos) {
    return (bs & ((uint64_t)1 << pos)) != 0;
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

// Find the position of the nth bit set
int bitset_nthset(bitset a, int n) {
    return __builtin_ffsl(_pdep_u64(1ULL << n, a)) - 1;
}
