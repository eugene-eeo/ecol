/*
 * graphcheck.c
 * ============
 * Fast filter similar to ecol graphcheck.
 */

#include "bitset.h"
#include "graph.h"
#include "graph6.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

typedef struct {
    graph* g;
    bitset core;
    bitset* adj;
    int* degree;
    int delta;
    int overfull;
} graphcheck;

// Deallocate
void graphcheck_free(graphcheck* gc) {
    graph_free(gc->g);
    free(gc->adj);
    free(gc->degree);

    gc->g = NULL;
    gc->adj = NULL;
    gc->degree = NULL;
    gc->delta = 0;
    gc->core = BITSET_INIT;
}

// Allocate core, adj, ... in response to graph
void graphcheck_alloc(graphcheck* gc) {
    gc->core = BITSET_INIT;
    gc->adj = calloc(gc->g->size, sizeof(bitset));
    gc->degree = calloc(gc->g->size, sizeof(int));
    gc->delta = graph_max_degree(gc->g);
}

// Update for new graph of same size
void graphcheck_update(graphcheck* gc) {
    gc->core = BITSET_INIT;
    for (int i = 0 ; i < gc->g->size; i++) {
        gc->degree[i] = 0;
        gc->adj[i] = BITSET_INIT;
    }
    // Actually update here
    gc->delta = graph_max_degree(gc->g);
    for (int u = 0; u < gc->g->size; u++) {
        gc->degree[u] = graph_get_degree(gc->g, u);
        if (gc->degree[u] == gc->delta) {
            gc->core = bitset_set(gc->core, u, 1);
        }
        for (int v = 0; v < gc->g->size; v++) {
            if (graph_get(gc->g, u, v) != -1) {
                gc->adj[u] = bitset_set(gc->adj[u], v, 1);
            }
        }
    }
    gc->overfull = (gc->g->num_uncoloured > (gc->delta) * (gc->g->size / 2));
}

int check_core_delta(graphcheck* gc, int deg) {
    int max = 0;
    for (int u = 0; u < gc->g->size; u++) {
        // Check that all core nodes u have
        // less than deg core nodes as neighbours
        if (gc->degree[u] == gc->delta) {
            int core_deg = bitset_count(bitset_intersection(gc->adj[u], gc->core));
            if (core_deg > deg)
                return 0;
            if (core_deg > max)
                max = core_deg;
        }
    }
    return max == deg;
}

int check_valid_semicore(graphcheck *gc) {
    // Check that all nodes in graph are either a
    // core node, or have a core node as neighbour
    for (int u = 0; u < gc->g->size; u++) {
        if (!bitset_intersection(gc->core, gc->adj[u])) {
            return 0;
        }
    }
    return 1;
}

char* help =
    "usage: gc [-d#] [-s] [-D#] [-o|-u] [-h]\n"
    "\n"
    "options:\n"
    "    -d# degree of core (0 = no check)\n"
    "    -s  check if valid semicore\n"
    "    -D# graph delta (0 = no check)\n"
    "    -o  only overfull\n"
    "    -u  only underfull\n"
    "    -h  help message\n";

int main(int argc, char* argv[]) {
    int opt;
    int core_delta = 0;
    int semicore = 0;
    int delta = 0;
    int overfull = 0;
    int underfull = 0;

    if (argc == 1) {
        printf("%s", help);
        exit(0);
    }

    while ((opt = getopt(argc, argv, "hd:sD:ou")) != -1) {
        switch (opt) {
            case 'h':
                printf("%s", help);
                exit(0);
                break;
            case 'd':
                core_delta = atoi(optarg);
                break;
            case 's':
                semicore = 1;
                break;
            case 'D':
                delta = atoi(optarg);
                break;
            case 'o':
                overfull = 1;
                break;
            case 'u':
                underfull = 1;
                break;
        }
    }

    // Main loop
    // graph
    graph g = graph_create(0);
    graphcheck gc;
    gc.g = &g;
    graphcheck_alloc(&gc);

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        if (gs.size != g.size) {
            graphcheck_free(&gc);
            g = graph_create(gs.size);
            gc.g = &g;
            graphcheck_alloc(&gc);
        }
        graph_clear(&g);
        graph6_write_graph(line, gs.cursor, gs.size, &g);
        graphcheck_update(&gc);

        const int valid =
            (overfull  ? gc.overfull  : 1) &&
            (underfull ? !gc.overfull : 1) &&
            (semicore  ? check_valid_semicore(&gc) : 1) &&
            (core_delta == 0 || check_core_delta(&gc, core_delta)) &&
            (delta == 0 || gc.delta == delta)
        ;
        if (valid)
            write(1, line, nbytes);
    }

    return 0;
}
