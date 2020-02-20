/*
 * lxc.c
 * =====
 *
 * lxc is a fast filter that takes in graph6 format graphs
 * and then emits them if they are class 2. usage example:
 *
 *     graph6-input | lxc | ...
 *
 */

#define  _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <getopt.h>

#include "bitset.h"
#include "graph.h"
#include "graph6.h"
#include "vizing_heuristic.h"

// Plaintext stream
// where graph is represented as n lines of n characters (0/1)
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
        u++;
        if (u == g.size)
            break;
    }

    g.num_uncoloured = g.num_uncoloured / 2;
    return g;
}

static const char* help =
    "usage: lxc [-a#] [-p] [-h]\n"
    "\n"
    "options:\n"
    "    -a# number of attempts (default: 15)\n"
    "    -p  plaintext format (default graph6)\n"
    "    -h  help message\n";

int showhelp(int code) {
    printf("%s", help);
    exit(code);
}

int main(int argc, char* argv[]) {
    srand(17021997);
    int opt;
    int pt;
    int attempts = 15;

    while ((opt = getopt(argc, argv, "ha:p")) != -1) {
        switch (opt) {
            case 'h':
                showhelp(0);
                break;
            case 'a':
                attempts = atoi(optarg);
                break;
            case 'p':
                pt = 1;
                break;
        }
    }

    if (pt) {
        graph g = pt_read_stream(stdin);
        int* P = allocate_path_array(&g);

        int delta = graph_max_degree(&g);
        bitset S = bitset_new(delta + 2);

        // do colouring
        graph_init(&g);

        int class1 = 0;
        int class2 = 0;
        int n = 0;

        for (int a = 0; a < attempts; a++) {
            n++;
            int class = vizing_heuristic(&g, P, delta, &S);
            switch (class) {
                case 1: class1++; break;
                case 2: class2++; break;
            }
            if (class == 1)
                break;
            for (int i = 0; i < g.size * g.size; i++) {
                g.edges[i] = g.edges[i] == -1 ? -1 : 0;
            }
        }

        printf("%f,%f\n", ((double) class1) / n, ((double) class2) / n);

        bitset_free(&S);
        free(P);

        graph_free(&g);
        exit(0);
    }

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);

        // Vizing
        graph g = graph_create(gs.size);
        int* P = allocate_path_array(&g);

        graph6_read_graph(line, gs.cursor, gs.size, &g);

        int class1 = 0;
        int delta = graph_max_degree(&g);
        bitset S = bitset_new(delta + 2);
        // Only do colouring if graph is underfull
        if (g.num_uncoloured <= delta * (g.size / 2)) {
            graph_init(&g);
            for (int a = 0; a < attempts; a++) {
                class1 = vizing_heuristic(&g, P, delta, &S) == 1;
                if (class1)
                    break;
                for (int i = 0; i < g.size * g.size; i++) {
                    g.edges[i] = g.edges[i] == -1 ? -1 : 0;
                }
            }
        }

        if (!class1)
            fwrite(line, sizeof(char), nbytes, stdout);

        bitset_free(&S);
        graph_free(&g);
        free(P);
    }

    fflush(stdout);
    if (line != NULL)
        free(line);
    return 0;
}
