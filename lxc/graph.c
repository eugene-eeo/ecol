/*
 * graph.c
 * =======
 *
 * Graph implementation and utility functions.
 *
 */

#include <stdlib.h>
#include "graph.h"

// Create a new graph
graph graph_create(int n) {
    graph g;
    g.edges = calloc(n * n, sizeof(int));

    for (int i = 0; i < n*n; i++) {
        g.edges[i] = -1;
    }

    g.free = NULL;
    g.size = n;
    g.num_uncoloured = 0;
    return g;
}

// Destroy graph
void graph_free(graph* g) {
    free(g->edges);
    if (g->free != NULL) {
        for (int i = 0; i < g->size; i++) {
            bitset_free(&g->free[i]);
        }
        free(g->free);
    }
}

// Finish initialization of graph
// Call when you are done setting up the graph
void graph_init(graph* g) {
    int delta = graph_max_degree(g);
    g->free = calloc(g->size, sizeof(bitset));
    for (int i = 0; i < g->size; i++) {
        // we never use 0 for colouring
        g->free[i] = bitset_new(delta + 2);
    }
}

// Set edge colour
void graph_set(graph* g, int u, int v, int colour) {
    int og = g->edges[(u * g->size) + v];

    g->edges[(u * g->size) + v] = colour;
    g->edges[(v * g->size) + u] = colour;

    if (og != 0) {
        if (og != -1) {
            bitset_set(&g->free[u], og, 1);
            bitset_set(&g->free[v], og, 1);
        }
        if (colour == 0) {
            g->num_uncoloured++;
        }
    }

    if (colour != 0) {
        bitset_set(&g->free[u], colour, 0);
        bitset_set(&g->free[v], colour, 0);
        if (og == 0) {
            g->num_uncoloured--;
        }
    }
}

// Get edge colour
int graph_get(graph* g, int u, int v) {
    return g->edges[u * g->size + v];
}

// Compute degree of node
int graph_get_degree(graph* g, int u) {
    int delta = 0;
    int n = g->size;
    int b = u * n;
    int* edges = g->edges;
    for (int i = 0; i < n; i++) {
        if (edges[b + i] != -1) {
            delta++;
        }
    }
    return delta;
}

// Find the next uncoloured edge
edge graph_next_uncoloured_edge(graph* g) {
    edge e = {-1, -1};
    int n = g->size;
    int* edges = g->edges;
    for (int i = 0; i < n; i++) {
        int m = i * n;
        for (int j = i + 1; j < n; j++) {
            if (edges[m + j] == 0) {
                e.i = i;
                e.j = j;
                return e;
            }
        }
    }
    return e;
}

// Compute max degree of graph
int graph_max_degree(graph* g) {
    int delta = 0;
    for (int u = 0; u < g->size; u++) {
        int d = graph_get_degree(g, u);
        if (d > delta)
            delta = d;
    }
    return delta;
}


// Utilities
int* allocate_path_array(graph* g) {
    return calloc(g->size, sizeof(int));
}

int _find_endpoint_with_colour(graph* g, int u, int colour) {
    int base = g->size * u;
    for (int v = 0; v < g->size; v++) {
        if (v != u && g->edges[base + v] == colour) {
            return v;
        }
    }
    return -1;
}

int get_path(graph* g, int v, int alpha, int beta, int* path) {
    path[0] = v;
    int swatch[2] = { beta, alpha };
    int length = 1;
    for (;;) {
        int endpoint = _find_endpoint_with_colour(
            g,
            path[length-1],
            swatch[length%2]
        );
        // No endpoint
        if (endpoint == -1) break;
        path[length] = endpoint;
        length++;
    }
    return length;
}

void switch_path(graph* g, int* path, int length, int alpha, int beta) {
    for (int i = 0; i < length - 1; i++) {
        graph_set(g, path[i], path[i+1], 0);
    }
    int swatch[2] = { beta, alpha };
    for (int i = 0; i < length - 1; i++) {
        graph_set(g, path[i], path[i+1], swatch[i % 2]);
    }
}

int verify_colouring(graph *g) {
    for (int i = 0; i < g->size; i++) {
        for (int j = i+1; j < g->size; j++) {
            // Check if (i, j) exists
            int c1 = graph_get(g, i, j);
            if (c1 == -1) continue;
            int k = i;
            for (int l = j+1; l < g->size; l++) {
                // we always return correct decision even if (k, l) == -1
                if (graph_get(g, k, l) == c1)
                    return 0;
            }
        }
    }
    return 1;
}

// Colours used in the graph
int colours_used(graph *g) {
    bitset bs = bitset_new(graph_max_degree(g) + 2);
    for (int i = 0; i < g->size; i++) {
        for (int j = i+1; j < g->size; j++) {
            bitset_set(&bs, graph_get(g, i, j), 1);
        }
    }
    int count = bitset_count(&bs);
    bitset_free(&bs);
    return count;
}
