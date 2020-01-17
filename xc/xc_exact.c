/*
 * xc_exact.c
 * ==========
 *
 * xce is slow as fucc lol
 *
 *     geng -c 5 | xce | ...
 *
 */

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "very_nauty/vn_graph.h"
#include "very_nauty/geng_reader.c"

int main() {
    char* s;
    graph_t g;
    while ((s = geng_getline(stdin))) {
        g = geng_stringtograph(s);

        // Now do exact colouring
        int delta = graph_max_degree(g);
        int overfull = nedges(g) > (nnodes(g) / 2) * delta;

        if (overfull || ( graph_edge_chromatic_number(g, 0) == delta + 1 ))
            write(1, s, strlen(s));

        if (s) free(s);
        graph_clear(g);
    }
}
