#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "bitset.h"
#include "graph.h"
#include "graph6.h"
#include "vizing_heuristic.h"

int main() {
    graph g = graph_create(0);
    char *line = NULL;
    size_t size;
    while (getline(&line, &size, stdin) != -1) {
        graph6_state gs = graph6_get_size(line);
        if (gs.size != g.size) {
            graph_free(&g);
            g = graph_create(gs.size);
        }
        graph6_write_graph(line, gs.cursor, gs.size, &g);
        int delta = graph_max_degree(&g);
        vizing_heuristic(&g);
        if (colours_used(&g) == delta + 1) {
            write(1, line, size);
        }
    }
}
