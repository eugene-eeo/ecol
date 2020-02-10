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
#include <getopt.h>

#include "graph.h"
#include "graph6.h"

// ==========
// Cycle-cycle Graph Family:
//  G(n) = Cn * C(n-1)

int cycle_cycle_graph_size(int n) {
    return n + (n - 1);
}

void cycle_cycle_graph(int n, graph* g) {
    // Create cycle on n nodes
    for (int i = 0; i < n - 1; i++) {
        graph_set(g, i, i+1, 0);
    }
    graph_set(g, n-1, 0, 0);

    // Create cycle on n-1 nodes
    int m = n + (n - 1);
    for (int i = n; i < m; i++) {
        graph_set(g, i, i+1, 0);
    }
    graph_set(g, m-1, n, 0);

    // Now Join
    for (int u = n; u < m; u++) {
        for (int v = 0; v < n; v++) {
            graph_set(g, u, v, 0);
        }
    }
}

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

// ==========
// Path-Path Graph Family:
//    G(n) = nP1 * (n-1)P1

int path_path_graph_size(int n) {
    return n + n - 1;
}

void path_path_graph(int n, graph* g) {
    // Join
    int end = path_path_graph_size(n);
    for (int u = 0; u < n; u++) {
        for (int v = n; v < end; v++) {
            graph_set(g, u, v, 0);
        }
    }
}

// ==========

static char* help =
    "usage: special [-h] [-p | -c | -C]\n"
    "\n"
    "options:\n"
    "    -h   help message\n"
    "    -p   path-path family  G(n) = nP1 * (n-1)P1\n"
    "    -c   path-cycle family G(n) = Cn * (n-1)P1\n"
    "    -C   cycle-cycle family G(n) = Cn * C(n-1)\n";

int showhelp(int code) {
    printf("%s", help);
    exit(code);
}

int main(int argc, char* argv[]) {
    int path_path = 0;
    int path_cycle = 0;
    int cycle_cycle = 0;

    int opt;
    while ((opt = getopt(argc, argv, "hpcC")) != -1) {
        switch (opt) {
            case 'h':
                showhelp(0);
                break;
            case 'p': path_path = 1; break;
            case 'c': path_cycle = 1; break;
            case 'C': cycle_cycle = 1; break;
        }
    }

    if (!path_path && !path_cycle && !cycle_cycle)
        showhelp(1);

    int size = cycle_cycle ? cycle_cycle_graph_size(30)
             : path_path   ? path_path_graph_size(30)
             :               cycle_path_graph_size(30);
    graph g = graph_create(size);
    char* buf = calloc(graph6_get_bytes_needed(g.size) + 1, sizeof(char));

    for (int n = 3; n <= 30; n++) {
        if (cycle_cycle)
            cycle_cycle_graph(n, &g);
        else if (path_path)
            path_path_graph(n, &g);
        else
            cycle_path_graph(n, &g);

        int m = cycle_cycle ? cycle_cycle_graph_size(n)
              : path_path   ? path_path_graph_size(n)
              : cycle_path_graph_size(n);
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
    graph_free(&g);
    return 0;
}
