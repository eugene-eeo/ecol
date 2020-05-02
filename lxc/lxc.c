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
#include <time.h>

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
            g = graph_create(nbytes - 1);
        }
        for (int i = 0; i < nbytes; i++) {
            if (line[i] == '1' || line[i] == '0') {
                g.edges[u * g.size + i] = line[i] == '1' ? 0 : -1;
            }
        }
        u++;
        if (u == g.size)
            break;
    }

    free(line);
    return g;
}

static const char* help =
    "usage: lxc [-a#] [-p] [-h] [-e] [-f]\n"
    "\n"
    "options:\n"
    "    -a# number of attempts (default: 15)\n"
    "    -p  plaintext format (default graph6)\n"
    "    -e  print out a matrix of edge colours (only makes sense with -p)\n"
    "    -f  compute full colouring (no short circuiting)\n"
    "    -h  help message\n";

int showhelp(int code) {
    printf("%s", help);
    exit(code);
}

int main(int argc, char* argv[]) {
    srand(17021997);
    int opt;
    int pt = 0;
    int attempts = 15;
    int output_edge_colouring = 0;
    int full_colouring = 0;

    while ((opt = getopt(argc, argv, "ha:pef")) != -1) {
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
            case 'e':
                output_edge_colouring = 1;
                break;
            case 'f':
                full_colouring = 1;
                break;
        }
    }

    // In pt mode we only read and edge-colour one graph
    // and then return the colours needed and time taken
    // for one run of the heuristic.
    if (pt) {
        graph g = pt_read_stream(stdin);
        if (g.size == 0)
            return 0;
        int* P = allocate_path_array(&g);

        int delta = graph_max_degree(&g);
        bitset S = bitset_new(delta + 2);

        // do colouring
        graph_init(&g);
        int class = 2;
        clock_t start = 0;
        clock_t stop = 0;

        bitset uncoloured = bitset_new(g.size * g.size);
        bitset_copy(&uncoloured, &g.uncoloured_edges);

        double total = 0;
        double num = 0;

        for (int a = 0; a < attempts; a++) {
            num += 1;
            start = clock();
            class = vizing_heuristic(&g, P, delta, &S, output_edge_colouring || full_colouring);
            stop = clock();
            total += (double)(stop - start) / CLOCKS_PER_SEC;
            /* if (class == 1 && !verify_colouring(&g)) */
            /*     printf("wtf!\n"); */
            if (class == 1)
                break;
            // do not clear the graph if we are on the last attempt
            if (a < attempts - 1) {
                bitset_copy(&g.uncoloured_edges, &uncoloured);
                for (int i = 0; i < g.size * g.size; i++) {
                    g.edges[i] = (g.edges[i] != -1) ? 0 : -1;
                }
            }
        }

        double avg_time = num > 0 ? total / num : 0;

        if (output_edge_colouring) {
            // Output the edge colouring as a matrix
            for (int u = 0; u < g.size; u++) {
                for (int v = 0; v < g.size; v++) {
                    printf("%d,", graph_get(&g, u, v));
                }
                printf("\n");
            }
        } else {
            printf("%d,%.2f\n",
                   (class == 1) ? delta : delta + 1, // colours needed
                   avg_time);       // average time
        }

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
        graph_init(&g);

        int class1 = 0;
        int delta = graph_max_degree(&g);
        int num_uncoloured = bitset_count(&g.uncoloured_edges) / 2;
        bitset S = bitset_new(delta + 2);
        // Only do colouring if graph is underfull
        if (num_uncoloured <= delta * (g.size / 2)) {
            bitset uncoloured = bitset_new(g.size * g.size);
            bitset_copy(&uncoloured, &g.uncoloured_edges);

            for (int a = 0; a < attempts; a++) {
                class1 = vizing_heuristic(&g, P, delta, &S, 0) == 1;
                if (class1)
                    break;
                bitset_copy(&g.uncoloured_edges, &uncoloured);
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
