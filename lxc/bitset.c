/*
 * bitset.c
 * ========
 *
 * Bitset implementation.
 *
 */

#include <stdlib.h>
#include "bitset.h"

// Tiny Bitsets (<= 64 values)
const bs_tiny BST_INIT = 0;

// Set bit pos to val
bs_tiny bst_set(bs_tiny bs, int pos, int val) {
    int64_t mask = (((uint64_t)1) << pos);
    if (val) {
        return bs | mask;
    } else {
        return bs & ~mask;
    }
}

// Test bit
int bst_test(bs_tiny bs, int pos) {
    return (bs & ((uint64_t)1 << pos)) != 0;
}

// Intersection of a and b
bs_tiny bst_intersection(bs_tiny a, bs_tiny b) {
    return a & b;
}

// Union between a and b
bs_tiny bst_union(bs_tiny a, bs_tiny b) {
    return a | b;
}

// Count the number of bits set
int bst_count(bs_tiny a) {
    return __builtin_popcountl(a);
}

// Find first set bit
int bst_first(bs_tiny a) {
    return __builtin_ffsl(a) - 1;
}


// Larger bitsets with dynamic memory allocation

// Create a new bitset
bitset bitset_new(int size) {
    bitset bs;
    bs.len = (size / 64) + 1;
    bs.B = calloc(bs.len, sizeof(bs_tiny));
    return bs;
}

// Free a bitset
void bitset_free(bitset *bs) {
    free(bs->B);
    bs->len = 0;
    bs->B = NULL;
}

void bitset_set(bitset *bs, int pos, int val) {
    bs->B[pos / 64] = bst_set(bs->B[pos / 64], pos % 64, val);
}

int bitset_test(bitset *bs, int pos) {
    return bst_test(bs->B[pos / 64], pos % 64);
}

void bitset_copy(bitset* dst, bitset* src) {
    // Copy
    for (int i = 0; i < src->len; i++)
        dst->B[i] = src->B[i];
    // Set remainder to 0
    for (int i = src->len; i < dst->len; i++)
        dst->B[i] = BST_INIT;
}

void bitset_intersection(bitset* dst, bitset* other) {
    for (int i = 0; i < other->len; i++)
        dst->B[i] = bst_intersection(dst->B[i], other->B[i]);
    // Set remainder to 0
    for (int i = other->len; i < dst->len; i++)
        dst->B[i] = BST_INIT;
}

void bitset_union(bitset* dst, bitset* other) {
    for (int i = 0; i < other->len; i++)
        dst->B[i] = bst_union(dst->B[i], other->B[i]);
    // Set remainder to 0
    for (int i = other->len; i < dst->len; i++)
        dst->B[i] = BST_INIT;
}

int bitset_count(bitset* bs) {
    int count = 0;
    for (int i = 0; i < bs->len; i++)
        count += bst_count(bs->B[i]);
    return count;
}

int bitset_first(bitset* bs) {
    int offset = 0;
    for (int i = 0; i < bs->len; i++) {
        int first = bst_first(bs->B[i]);
        if (first != -1)
            return first + offset;
        offset += 64;
    }
    return -1;
}

void bitset_clear(bitset* bs) {
    for (int i = 0; i < bs->len; i++)
        bs->B[i] = BST_INIT;
}
