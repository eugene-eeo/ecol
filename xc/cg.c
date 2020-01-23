/*
 * cg.c
 * ====
 *
 * Generate semicores around the given cores.
 * Only generates graphs <= 62 nodes.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <time.h>

#include "graph.h"
#include "graph6.h"

// get a random number in the range of [m,n]
int randrange(int m, int n) {
    return m + rand() / (RAND_MAX / (n - m + 1) + 1);
}

typedef struct {
    int created;
    graph g;
} maybe_graph;

// extend core
maybe_graph extend_core(graph core, int maxn, int delta, int attempts) {
    maybe_graph m;
    for (int i = 0; i < attempts; i++) {
        int n = randrange(core.size + 1, maxn);
        graph g = graph_create(n);
        // Allowed # neighbours per node
        int* allowed = calloc(n, sizeof(int));

        int ok = 1;
        graph_clear(&g);
        // Copy core over
        for (int u = 0; u < core.size; u++) {
            for (int v = u+1; v < core.size; v++) {
                graph_set(&g, u, v, graph_get(&core, u, v));
            }
        }

        // For the existing core
        for (int u = 0; u < core.size; u++)
            allowed[u] = delta - graph_get_degree(&g, u);

        // New nodes
        for (int u = core.size; u < g.size; u++)
            allowed[u] = randrange(1, delta - 1);

        // Link new nodes
        for (int u = core.size; u < g.size; u++) {
            if (allowed[u] == 0) continue;
            int core_count = randrange(1, allowed[u]); // # core nodes
            int other = allowed[u] - core_count;       // # other nodes

            // Links to core
            for (int i = 0; i < core_count; i++) {
                int set = 0;
                for (int a = 0; a < core.size; a++) {
                    int v = randrange(0, core.size - 1);
                    if (allowed[v] == 0 || graph_get(&g, u, v) == 0) continue;
                    // Otherwise add this link
                    graph_set(&g, u, v, 0);
                    allowed[u]--;
                    allowed[v]--;
                    set = 1;
                    break;
                }
                if (!set) break;
            }

            // Links to other nodes
            for (int i = 0; i < other; i++) {
                int set = 0;
                for (int a = 0; a < n - core.size; a++) {
                    int v = randrange(core.size, g.size - 1);
                    if (allowed[v] == 0 || graph_get(&g, u, v) == 0) continue;
                    // Otherwise add this link
                    graph_set(&g, u, v, 0);
                    allowed[u]--;
                    allowed[v]--;
                    set = 1;
                    break;
                }
                if (!set) break;
            }
        }

        // Check that it's valid!
        for (int i = 0; i < g.size; i++) {
            // For core nodes, degree needs to be delta
            // otherwise degree needs to be > 0
            int deg = graph_get_degree(&g, i);
            if (i < core.size
                    ? (deg != delta)
                    : (deg == 0 || deg == delta)) {
                ok = 0;
                break;
            }
        }

        free(allowed);
        if (ok) {
            m.g = g;
            m.created = 1;
            return m;
        }
        // Otherwise we need to free g
        graph_free(&g);
    }
}

char* help =
    "usage: cg [-h] [-S#] [-a#] [-n#] -N# -d#\n"
    "\n"
    "options:\n"
    "    -S# seed rng (default = time.time)\n"
    "    -a# attempts (default = 10000)\n"
    "    -d# degree of semicores\n"
    "    -N# max number of nodes per semicore\n"
    "    -n# number of random semicores per core (default = 100)\n"
    "    -h  help message\n";

int showhelp(int code) {
    printf("%s", help);
    exit(code);
}

int main(int argc, char* argv[]) {
    int opt;
    int delta = 0;
    int nodes_per_semicore = 0;
    int semicores_per_core = 100;
    int seed = time(NULL) ^ getpid();
    int attempts = 10000;

    while ((opt = getopt(argc, argv, "hS:a:n:N:d:")) != -1) {
        switch (opt) {
            case 'h':
                showhelp(0);
                break;
            case 'd':
                delta = atoi(optarg);
                break;
            case 'N':
                nodes_per_semicore = atoi(optarg);
                break;
            case 'n':
                semicores_per_core = atoi(optarg);
                break;
            case 'S':
                seed = atoi(optarg);
                break;
            case 'a':
                attempts = atoi(optarg);
                break;
        }
    }

    if (nodes_per_semicore == 0 || delta == 0 || delta >= nodes_per_semicore)
        showhelp(1);

    srand(seed);

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        graph core = graph_create(gs.size);
        graph6_write_graph(line, gs.cursor, gs.size, &core);

        if (core.size + 1 < nodes_per_semicore) {
            for (int i = 0; i < semicores_per_core; i++) {
                maybe_graph m = extend_core(core, nodes_per_semicore, delta, attempts);
                if (!m.created)
                    continue;
                int n = graph6_get_bytes_needed(m.g);

                char* buf = calloc(n + 1, sizeof(char));
                graph6_write_bytes(m.g, buf, n);
                buf[n] = '\n';

                write(1, buf, n+1);
                graph_free(&m.g);
                free(buf);
            }
        }
        graph_free(&core);
    }

    if (line != NULL)
        free(line);
}
