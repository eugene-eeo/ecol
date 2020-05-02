/*
 * vizing_heuristic.c
 * ==================
 *
 * Implementation of the vizing heuristic.
 *
 */

#include "bitset.h"
#include "graph.h"
#include "vizing_heuristic.h"
#include <stdlib.h>

// get a random number in the range of [0,n)
int randrange(int n) {
    return rand() / (RAND_MAX / (double)n + 1);
    // [0, n]
    // return rand() / (RAND_MAX / (n + 1) + 1);
}

int bitset_nthset_with_index(bitset* bs, int n, int* idx) {
    int run = 0;
    for (int i = 0; i < bs->len; i++) {
        bs_tiny b = bs->B[i];
        int count = bst_count(b);
        if (count + run > n) {
            *idx = i;
            return 64*i + bst_nthset(b, n - run);
        }
        run += count;
    }
    return -1;
}

int sample(bitset* bs) {
    return bitset_nthset(bs, randrange(bitset_count(bs)));
}

int sample_bst(bitset* bs, int *idx) {
    int u = *idx;
    int n = bs->len;
    bs_tiny* B = bs->B;
    // sample from different region
    if (rand() <= 0.0625 || bst_count(B[u]) == 0) {
        // sample at most 100 places; otherwise fallback to
        // locality-insensitive sample.
        int ok = 0;
        int k = randrange(n);
        for (int i = 0; i < 100; i++) {
            u = (u + i*k) % n;
            if (bst_count(B[u]) > 0) {
                *idx = u;
                ok = 1;
                break;
            }
        }
        if (!ok) {
            return bitset_nthset_with_index(bs, randrange(bitset_count(bs)), idx);
        }
    }
    bs_tiny b = B[u];
    return (64*u) + bst_nthset(b, randrange(bst_count(b)));
}

int vizing_heuristic(graph* g, int* P, int delta, bitset* S, int full) {
    bitset_clear(S);
    // Set available colours to delta
    for (int colour = 1; colour <= delta; colour++) {
        bitset_set(S, colour, 1);
    }
    for (int i = 0; i < g->size; i++)
        bitset_copy(&g->free[i], S);

    int idx = 0;
    int class = 1;
    int taboo = 0;
    int w = -1;
    int v_0 = -1;
    int beta = 0;

    // S is used throughout code
    bitset_clear(S);

    while (bitset_any(&g->uncoloured_edges)) {
        if (taboo == 0) {
            int pos = sample_bst(&g->uncoloured_edges, &idx);
            /* int pos = sample(&g->uncoloured_edges); */
            w   = pos / g->size;
            v_0 = pos % g->size;
            /* printf("(%d,%d,%d)\n", w, v_0, graph_get(g, w, v_0)); */
        }

        // S = Free[w] ^ Free[v_0]
        bitset_copy(S, &g->free[w]);
        bitset_intersection(S, &g->free[v_0]);

        if (bitset_any(S)) {
            int colour = bitset_first(S);
            graph_set(g, w, v_0, colour);
            taboo = 0;
        } else {
            // Check if free[v_0] has some colour != taboo
            bitset_copy(S, &g->free[v_0]);
            bitset_set(S, taboo, 0);

            if (!bitset_any(S)) {
                // Whether we need to compute a full, proper edge colouring
                // or do we just need the class estimate
                if (full) {
                    for (int i = 0; i < g->size; i++) {
                        bitset_set(&g->free[i], delta + 1, 1);
                    }
                    graph_set(g, w, v_0, delta + 1);
                    taboo = 0;
                    class = 2;
                } else {
                    return 2;
                }
            } else {
                int alpha = bitset_first(S);
                if (taboo == 0) {
                    beta = bitset_first(&g->free[w]);
                }
                int len = get_path(g, v_0, beta, alpha, P);
                if (P[len-1] != w) {
                    switch_path(g, P, len, beta, alpha);
                    graph_set(g, w, v_0, beta);
                    taboo = 0;
                } else {
                    int a = P[len-2];
                    graph_set(g, w, a, 0);
                    graph_set(g, w, v_0, alpha);
                    v_0 = a;
                    taboo = alpha;
                }
            }
        }
    }
    return class;
}
