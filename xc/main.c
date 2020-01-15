#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "bitset.h"
#include "graph.h"
#include "graph6.h"
#include "vizing_heuristic.h"

int main() {
    graph g = graph_create(0);
    int* P = allocate_path_array(&g);
    char* line = NULL;
    size_t size;
    ssize_t nbytes;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        if (gs.size != g.size) {
            graph_free(&g);
            free(P);
            g = graph_create(gs.size);
            P = allocate_path_array(&g);
        }

        g.num_uncoloured = 0;
        graph6_write_graph(line, gs.cursor, gs.size, &g);
        if (vizing_heuristic(&g, P) == 2) {
            write(1, line, nbytes);
        }
    }
}
