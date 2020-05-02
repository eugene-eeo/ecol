#ifndef BITSET_H
#define BITSET_H

#include <inttypes.h>

typedef int64_t bs_tiny;
extern const bs_tiny BST_INIT;

typedef struct {
    int len;
    bs_tiny* B;
} bitset;

int bst_count(bs_tiny a);
int bst_nthset(bs_tiny a, int n);

bitset bitset_new(int size);
void bitset_free(bitset* bs);
void bitset_set(bitset* bs, int pos, int val);
int bitset_test(bitset* bs, int pos);

void bitset_copy(bitset* dst, bitset* src);
void bitset_intersection(bitset* dst, bitset *other);
void bitset_union(bitset* dst, bitset* other);
void bitset_clear(bitset* bs);

int bitset_any(bitset* bs);
int bitset_count(bitset* bs);
int bitset_first(bitset* bs);
int bitset_nthset(bitset* bs, int n);

#endif /* BITSET_H */
