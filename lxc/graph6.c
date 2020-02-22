#include "graph.h"
#include "graph6.h"
#include <stdio.h>

// Get size of the graph and a cursor
graph6_state graph6_get_size(char* data) {
    graph6_state s;
    int m = 0;
    for (int i = 0; i < 3; i++) {
        if (data[i] == 126) {
            m++;
        } else {
            break;
        }
    }
    // 3 cases for m:
    // (0) N(n) = n+63         [1 byte]
    // (1) N(n) = 126 R(n)     [4 bytes]
    // (2) N(n) = 126 126 R(n) [8 bytes]
    switch (m) {
    case 0: s.cursor = 1; break;
    case 1: s.cursor = 4; break;
    case 2: s.cursor = 8; break;
    }
    int size = 0;
    for (int i = m; i < s.cursor; i++) {
        size += (1 << (6 * (s.cursor - i - 1))) * (data[i] - 63);
    }
    s.size = size;
    return s;
}

void graph6_read_graph(char* data, int cursor, int size, graph* g) {
    int k = 0;
    for (int v = 0; v < size; v++) {
        for (int u = 0; u < v; u++) {
            int b = (data[cursor + (k / 6)] - 63) << 2;
            int m = (1 << (7 - k%6));
            /* graph_set(g, u, v, (b & m) ? 0 : -1); */
            int c = (b & m) ? 0 : -1;
            g->edges[u * size + v] = c;
            g->edges[v * size + u] = c;
            k++;
        }
    }
}
