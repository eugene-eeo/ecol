// Only handles graphs of size <= 62

#include "graph.h"
#include "graph6.h"

// Get size of the graph and a cursor
graph6_state graph6_get_size(char* data) {
    graph6_state s = { 0, 0 };
    s.cursor = 1;
    s.size = data[0] - 63;
    return s;
}

void graph6_write_graph(char* data, int cursor, int size, graph* g) {
    int k = 0;
    for (int v = 0; v < size; v++) {
        for (int u = 0; u < v; u++) {
            int b = (data[cursor + (k / 6)] - 63) << 2;
            int m = (1 << (7 - k%6));
            /* graph_set(g, u, v, (b & m) ? 0 : -1); */
            int c = (b & m) ? 0 : -1;
            g->edges[u * size + v] = c;
            g->edges[v * size + u] = c;
            if (c == 0)
                g->num_uncoloured++;
            k++;
        }
    }
}

int graph6_get_bytes_needed(graph g) {
    // N(x)
    int n = 1;
    // R(X)
    int r = 0;
    return n;
}
