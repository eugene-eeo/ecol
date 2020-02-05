// Only handles graphs of size <= 62

#include "graph.h"
#include "graph6.h"
#include <stdio.h>

// Get size of the graph and a cursor
graph6_state graph6_get_size(char* data) {
    graph6_state s;
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

// Bytes needed to write graph of size n
int graph6_get_bytes_needed(int n) {
    // N(x)
    int N = 1;
    int edges = (n * (n - 1)) / 2;
    int R = edges / 6 + (edges % 6 > 0); // R(X) = ceil(#edges / 6)
    return N + R;
}

void graph6_write_bytes(graph g, int n, char* buf) {
    // Write size
    buf[0] = n;

    // Write R(x)
    int k = 0;
    for (int v = 0; v < n; v++) {
        for (int u = 0; u < v; u++) {
            int i = k / 6;
            int j = 5 - (k % 6);
            if (graph_get(&g, u, v) == -1) {
                buf[i + 1] &= ~((char)1 << j);
            } else {
                buf[i + 1] |= ((char)1 << j);
            }
            k++;
        }
    }

    // remember to add 63 to all bytes
    int b = graph6_get_bytes_needed(n);
    for (int i = 0; i < b; i++) {
        buf[i] += 63;
    }
}
