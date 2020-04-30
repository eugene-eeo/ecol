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
    return rand() / (RAND_MAX / n + 1);
    // [0, n]
    // return rand() / (RAND_MAX / (n + 1) + 1);
}

int sample(bitset* bs) {
    return bitset_nthset(bs, randrange(bitset_count(bs)));
}

int vizing_heuristic(graph* g, int* P, int delta, bitset* S) {
    bitset_clear(S);
    // Set available colours to delta
    for (int colour = 1; colour <= delta; colour++) {
        bitset_set(S, colour, 1);
    }
    for (int i = 0; i < g->size; i++)
        bitset_copy(&g->free[i], S);

    int taboo = 0;
    int w = -1;
    int v_0 = -1;
    int beta = 0;

    // S is used throughout code
    bitset_clear(S);

    while (bitset_any(&g->uncoloured_edges)) {
        if (taboo == 0) {
            /* int pos = sample(&g->uncoloured_edges); */
            /* w   = pos / g->size; */
            /* v_0 = pos % g->size; */
            edge e = graph_next_uncoloured_edge(g);
            w = e.i;
            v_0 = e.j;
        }

        // S = Free[w] ^ Free[v_0]
        bitset_copy(S, &g->free[w]);
        bitset_intersection(S, &g->free[v_0]);

        if (bitset_any(S)) {
            int colour = sample(S);
            graph_set(g, w, v_0, colour);
            taboo = 0;
        } else {
            // Check if free[v_0] has some colour != taboo
            bitset_copy(S, &g->free[v_0]);
            bitset_set(S, taboo, 0);

            if (!bitset_any(S)) {
                /* for (int i = 0; i < g->size; i++) { */
                /*     bitset_set(&g->free[i], delta + 1, 1); */
                /* } */
                /* graph_set(g, w, v_0, delta + 1); */
                /* taboo = 0; */
                /* class = 2; */
                return 2;
            } else {
                int alpha = sample(S);
                if (taboo == 0) {
                    beta = sample(&g->free[w]);
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
    return 1;
}
