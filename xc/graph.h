#ifndef GRAPH_H
#define GRAPH_H

#include "bitset.h"

typedef struct {
    int size;
    int *edges;
    int num_uncoloured;
    bitset* free; // Free colours for a node
} graph;

typedef struct {
    int i;
    int j;
} edge;

// Graph functions
graph graph_create(int n);
void graph_free(graph* g);
void graph_set(graph* g, int u, int v, int colour);
int graph_get(graph* g, int u, int v);
int graph_get_degree(graph* g, int u);
edge graph_next_uncoloured_edge(graph* g);
int graph_max_degree(graph* g);
void graph_clear(graph* g);

// Utilities
int* allocate_path_array(graph* g);
int get_path(graph* g, int v, int alpha, int beta, int* path);
void switch_path(graph* g, int* path, int length, int alpha, int beta);
int verify_colouring(graph* g);
int colours_used(graph* g);

#endif /* GRAPH_H */
