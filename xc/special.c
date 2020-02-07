/*
 * special.c
 * =========
 *
 * ad hoc generation of families of special graphs
 */

#define  _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "graph.h"
#include "graph6.h"

// ==========
// Cycle-Path Graph Family:
//  G(n) = Cn * (n-1)P1

int cycle_path_graph_size(int n) {
    return n + (n - 1);
}

void cycle_path_graph(int n, graph* g) {
    // Create cycle on n nodes
    for (int i = 0; i < n - 1; i++) {
        graph_set(g, i, i+1, 0);
    }
    graph_set(g, n-1, 0, 0);

    // Now Join
    int m = n + (n - 1);
    for (int u = n; u < m; u++) {
        for (int v = 0; v < n; v++) {
            graph_set(g, u, v, 0);
        }
    }
}

// ==========

int main() {
    graph g = graph_create(cycle_path_graph_size(30));
    char* buf = calloc(graph6_get_bytes_needed(g.size) + 1, sizeof(char));

    for (int n = 3; n <= 30; n++) {
        cycle_path_graph(n, &g);

        int m = cycle_path_graph_size(n);
        int b = graph6_get_bytes_needed(m);

        memset(buf, 0, b);
        graph6_write_bytes(g, m, buf);
        buf[b] = '\n';
        fwrite(buf, sizeof(char), b+1, stdout);

        // Clear for next iteration
        graph_clear(&g);
    }

    fflush(stdout);
    free(buf);
    return 0;
}
