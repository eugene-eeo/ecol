#include <stdio.h>
#include "bitset.h"
#include "graph.h"
#include "vizing_heuristic.h"

int main() {
    bitset bs = BITSET_INIT;
    /* bs = bitset_set(bs, 0, 1); */
    /* bs = bitset_set(bs, 1, 1); */
    bs = bitset_set(bs, 63, 1);
    printf("%ld\n", bs);
    printf("%d\n", bitset_count(bs));
    printf("%d\n", bitset_first(bs));

    graph g = graph_create(10);
    graph_set(&g, 0, 1, 1);
    graph_set(&g, 2, 3, 0);
    edge e = graph_next_uncoloured_edge(&g);

    printf("%d,%d\n", e.i, e.j);
    printf("%d\n", graph_max_degree(&g));

    // =====================

    graph h = graph_create(10);
    for (int i = 0; i < h.size; i++) {
        for (int j = i + 1; j < h.size; j++) {
            graph_set(&h, i, j, 0);
        }
    }
    printf("%d\n", h.num_uncoloured);
    vizing_heuristic(&h);
}
