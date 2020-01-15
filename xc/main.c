#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "bitset.h"
#include "graph.h"
#include "graph6.h"
#include "vizing_heuristic.h"

const int ATTEMPTS = 10;

// xorshift prng
typedef struct xorshift64s_state {
  uint64_t a;
} xorshift64s_state;

uint64_t xorshift64s(xorshift64s_state *state)
{
    uint64_t x = state->a;	/* The state must be seeded with a nonzero value. */
    x ^= x >> 12; // a
    x ^= x << 25; // b
    x ^= x >> 27; // c
    state->a = x;
    return x * UINT64_C(0x2545F4914F6CDD1D);
}

void shuffle(xorshift64s_state *state, int* x, int n) {
    int i, j, tmp;
    for (i = n - 1; i > 0; i--) {
        j = xorshift64s(state) % (i + 1);
        tmp = x[j];
        x[j] = x[i];
        x[i] = tmp;
    }
}

void remap(xorshift64s_state *state, int* map, int* ed, graph* g, int num_uncoloured) {
    // shuffle array
    shuffle(state, map, g->size);
    int n = g->size;
    for (int i = 0; i < n*n; i++) {
        ed[i] = (g->edges[i] == -1) ? -1 : 0;
    }
    for (int u = 0; u < g->size; u++) {
        for (int v = 0; v < g->size; v++) {
            int I = n * u      + v;
            int J = n * map[u] + map[v];
            g->edges[I] = ed[J];
        }
    }
    g->num_uncoloured = num_uncoloured;
}

void init_map(int* map, int size) {
    for (int i = 0; i < size; i++)
        map[i] = i;
}

int main() {
    // vizing
    graph g = graph_create(0);
    int* P = allocate_path_array(&g);

    // Remap
    int* map = calloc(0, sizeof(int));
    xorshift64s_state state = { 42 };
    int* ed = calloc(0, sizeof(int)); // Edge data for remap

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        if (gs.size != g.size) {
            graph_free(&g);
            free(P);
            free(map);
            free(ed);
            g = graph_create(gs.size);
            P = allocate_path_array(&g);
            map = calloc(gs.size, sizeof(int));
            init_map(map, gs.size);
            ed = calloc(gs.size * gs.size, sizeof(int));
        }

        graph_clear(&g);
        g.num_uncoloured = 0;
        graph6_write_graph(line, gs.cursor, gs.size, &g);

        int class1 = 0;
        // Only do colouring if graph is underfull
        if (g.num_uncoloured <= graph_max_degree(&g) * (g.size / 2)) {
            int num_uncoloured = g.num_uncoloured;
            for (int a = 0; a < ATTEMPTS; a++) {
                class1 = vizing_heuristic(&g, P) == 1;
                if (class1)
                    break;
                remap(&state, map, ed, &g, num_uncoloured);
            }
        }

        if (!class1)
            write(1, line, nbytes);
    }
}
