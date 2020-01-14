#ifndef BITSET_H
#define BITSET_H

#include <inttypes.h>

typedef int64_t bitset;
extern const bitset BITSET_INIT;

bitset bitset_set(bitset bs, int pos, int val);
int bitset_test(bitset bs, int pos);
bitset bitset_intersection(bitset a, bitset b);
bitset bitset_union(bitset a, bitset b);
int bitset_count(bitset a);
int bitset_first(bitset a);

#endif /* BITSET_H */
