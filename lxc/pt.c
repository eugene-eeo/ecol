#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

graph pt_read_stream(FILE* f) {
    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    // Graph
    int u = 0;
    graph g;

    while ((nbytes = getline(&line, &size, f)) > 0) {
        if (u == 0) {
            g = graph_create(nbytes);
        }
        for (int i = 0; i < nbytes; i++) {
            if (line[i] == '1' || line[i] == '0') {
                g.edges[u * g.size + i] = line[i] == '1' ? 0 : -1;
                if (line[i] == '1')
                    g.num_uncoloured++;
            }
        }
    }

    g.num_uncoloured = g.num_uncoloured / 2;
    return g;
}
