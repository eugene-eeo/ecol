/*
 * gc.c
 * ====
 * Fast filter similar to ecol graphcheck.
 * Usage:
 *
 *    geng -c 8 | gc -u | ...
 *
 * Only use if the graphs have size <= 62.
 */

#define  _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

#include "bitset.h"
#include "graph.h"
#include "graph6.h"

typedef struct {
    graph* g;
    bitset core;
    bitset* adj;
    int* degree;
    int delta;
    int overfull;
} graphcheck;

// Deallocate
void graphcheck_free(graphcheck* gc, int need_advanced) {
    graph_free(gc->g);
    if (need_advanced) {
        free(gc->adj);
        free(gc->degree);
    }

    gc->g = NULL;
    gc->adj = NULL;
    gc->degree = NULL;
    gc->delta = 0;
    gc->core = BITSET_INIT;
}

// Allocate core, adj, ... in response to graph
void graphcheck_alloc(graphcheck* gc, int need_advanced) {
    if (need_advanced) {
        gc->core = BITSET_INIT;
        gc->adj = calloc(gc->g->size, sizeof(bitset));
        gc->degree = calloc(gc->g->size, sizeof(int));
    }
    gc->delta = 0;
}

// Update for new graph of same size
void graphcheck_update(graphcheck* gc, int need_advanced) {
    gc->delta = graph_max_degree(gc->g);
    if (need_advanced) {
        // Clear old data
        gc->core = BITSET_INIT;
        for (int i = 0 ; i < gc->g->size; i++) {
            gc->degree[i] = 0;
            gc->adj[i] = BITSET_INIT;
        }
        // Actually update here
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
        if (gc->degree[u] != gc->delta && !bitset_intersection(gc->core, gc->adj[u])) {
            return 0;
        }
    }
    return 1;
}

int dfs(int u, bitset* visited, graph g, int parent) {
    *visited = bitset_set(*visited, u, 1);
    for (int v = 0; v < g.size; v++) {
        if (v != u && v != parent && graph_get(&g, u, v) != -1) {
            if (bitset_test(*visited, v)) return 1;
            if (dfs(v, visited, g, u)) return 1;
        }
    }
    return 0;
}

int has_cycle(graph g) {
    bitset visited = BITSET_INIT;
    for (int u = 0; u < g.size; u++) {
        if (bitset_test(visited, u)) continue;
        if (dfs(u, &visited, g, -1)) return 1;
        return 0;
    }
    return 0;
}

static const char* help =
    "usage: gc [-d#] [-s] [-c] [-D#] [-o|-u] [-h]\n"
    "\n"
    "options:\n"
    "    -d# degree of core (0 = no check)\n"
    "    -s  check if valid semicore\n"
    "    -c  check if graph contains cycle\n"
    "    -D# graph delta (0 = no check)\n"
    "    -o  only overfull\n"
    "    -u  only underfull\n"
    "    -h  help message\n";

int showhelp(int code) {
    printf("%s", help);
    exit(code);
}

int main(int argc, char* argv[]) {
    int opt;
    int core_delta = 0;
    int semicore = 0;
    int delta = 0;
    int overfull = 0;
    int underfull = 0;
    int contains_cycle = 0;

    while ((opt = getopt(argc, argv, "hd:scD:ou")) != -1) {
        switch (opt) {
            case 'h':
                showhelp(0);
                break;
            case 'd':
                core_delta = atoi(optarg);
                break;
            case 's':
                semicore = 1;
                break;
            case 'c':
                contains_cycle = 1;
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

    if (!contains_cycle && !core_delta && !semicore && !delta && !overfull && !underfull)
        showhelp(1);

    // Whether we need allocations for adj and core
    int need_advanced = core_delta || semicore;

    // Main loop
    // graph
    graph g = graph_create(1);
    graphcheck gc;
    gc.g = &g;
    graphcheck_alloc(&gc, need_advanced);

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        if (gs.size != g.size) {
            graphcheck_free(&gc, need_advanced);
            g = graph_create(gs.size);
            gc.g = &g;
            graphcheck_alloc(&gc, need_advanced);
        }
        graph_clear(&g);
        graph6_write_graph(line, gs.cursor, gs.size, &g);
        graphcheck_update(&gc, need_advanced);

        const int valid =
            (!overfull       || gc.overfull) &&
            (!underfull      || !gc.overfull) &&
            (!contains_cycle || has_cycle(g)) &&
            (!semicore       || check_valid_semicore(&gc)) &&
            (core_delta == 0 || check_core_delta(&gc, core_delta)) &&
            (delta == 0      || gc.delta == delta)
        ;
        if (valid)
            fwrite(line, sizeof(char), nbytes, stdout);
    }

    fflush(stdout);
    return 0;
}
