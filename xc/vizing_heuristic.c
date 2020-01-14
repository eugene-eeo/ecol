/*
 * vizing_heuristic.c
 * ==================
 *
 * Implementation of the vizing heuristic.
 *
 */

// We won't be using the algorithm on graphs with degrees or
// node counts more than 64, so it's fine to use the int64
// bitset.
#include "bitset.h"
#include "graph.h"
#include "vizing_heuristic.h"
#include <stdio.h>

void vizing_heuristic(graph* g) {
    int delta = graph_max_degree(g);
    bitset colours = BITSET_INIT;
    for (int i = 0; i <= delta; i++) {
        colours = bitset_set(colours, i, 1);
    }

    // Set available colours to delta
    bitset bs = (int64_t) (1 << (delta+1)) - 2;
    for (int i = 0; i < g->size; i++) {
        g->free[i] = bs;
    }

    int taboo = 0;
    int w = -1;
    int v_0 = -1;
    int beta = 0;
    int* P = allocate_path_array(g);
    bitset S = BITSET_INIT;

    while (g->num_uncoloured > 0) {
        if (taboo == 0) {
            edge e = graph_next_uncoloured_edge(g);
            w = e.i;
            v_0 = e.j;
        }

        // Clear
        S = bitset_intersection(g->free[w], g->free[v_0]);
        if (S) {
            int colour = bitset_first(S);
            graph_set(g, w, v_0, colour);
        } else {
            // Check if free[v_0] has some colour != taboo
            S = bitset_set(g->free[v_0], taboo, 0);
            if (!S) {
                for (int i = 0; i < g->size; i++) {
                    g->free[i] = bitset_set(g->free[i], delta+1, 1);
                }
                graph_set(g, w, v_0, delta+1);
                taboo = 0;
            } else {
                int alpha = bitset_first(S);
                if (taboo == 0) {
                    beta = bitset_first(g->free[w]);
                }
                int len = get_path(g, v_0, beta, alpha, P);
                if (P[len-1] != w) {
                    switch_path(g, P, len, beta, alpha);
                    graph_set(g, w, v_0, beta);
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
}
