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

// Bytes needed to write graph of size n
int graph6_get_bytes_needed(int n) {
    int N = 1;
    if (n <= 62) {
        N = 1;
    } else if (n <= 258047) {
        N = 4;
    } else {
        N = 8;
    }
    int edges = (n * (n - 1)) / 2;
    int R = edges / 6 + (edges % 6 > 0); // R(x) = ceil(#edges / 6)
    return N + R;
}

void graph6_write_bytes(graph g, int n, char* buf) {
    // Write size
    int N = 1;
    if (n <= 62) {
        N = 1;
        buf[0] = n;
    } else if (n <= 258047) {
        N = 4;
        buf[0] = 126;
        buf[1] = (n >> 12) & 63;
        buf[2] = (n >> 6) & 63;
        buf[3] = n & 63;
    } else {
        N = 8;
        buf[0] = 126;
        buf[1] = 126;
        buf[2] = (n >> 30) & 63;
        buf[3] = (n >> 24) & 63;
        buf[4] = (n >> 18) & 63;
        buf[5] = (n >> 12) & 63;
        buf[6] = (n >> 6)  & 63;
        buf[7] = n         & 63;
    }

    // Write R(x)
    int k = 0;
    for (int v = 0; v < n; v++) {
        for (int u = 0; u < v; u++) {
            int i = k / 6;
            int j = 5 - (k % 6);
            if (graph_get(&g, u, v) == -1) {
                buf[N + i] &= ~((char)1 << j);
            } else {
                buf[N + i] |= ((char)1 << j);
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
