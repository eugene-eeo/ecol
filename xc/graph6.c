#include "graph.h"
#include "graph6.h"

// Get size of the graph and a cursor
graph6_state graph6_get_size(char* data) {
    int m = 0;
    for (int i = 0; i < 2; i++) {
        if (data[i] == 126) {
            m++;
        } else {
            break;
        }
    }
    graph6_state s = { 0, 0 };
    // 3 cases for m:
    // (0) N(n) = n+63         [1 bytes]
    // (1) N(n) = 126 R(x)     [4 bytes]
    // (2) N(n) = 126 126 R(x) [8 bytes]
    switch (m) {
        case 0: s.cursor = 1; break;
        case 1: s.cursor = 4; break;
        case 2: s.cursor = 8; break;
    }
    for (int i = m; i < s.cursor; i++) {
        s.size += data[i] - 63;
    }
    return s;
}

void graph6_write_graph(char* data, int cursor, int size, graph* g) {
    int k = 0;
    for (int v = 0; v < size; v++) {
        for (int u = 0; u < v; u++) {
            int b = (data[cursor + (k / 6)] - 63) << 2;
            int m = (1 << (7 - k%6));
            graph_set(g, u, v, (b & m) ? 0 : -1);
            k++;
        }
    }
}
