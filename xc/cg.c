/*
 * cg.c
 * ====
 *
 * Generate semicores around the given cores.
 * Only generates graphs <= 62 nodes.
 *
 */

#define  _GNU_SOURCE
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <time.h>

#include "graph.h"
#include "graph6.h"
#include "bitset.h"

// get a random number in the range of [m,n]
int randrange(int m, int n) {
    return m + rand() / (RAND_MAX / (n - m + 1) + 1);
}

// extend core
int extend_core(graph core, int maxn, int delta, int attempts, int* allowed, graph* g, bitset* adj) {
    // Bitset where bits 0..core.size-1 are all set
    bitset core_adj = (((bitset) 1) << core.size) - 1;
    for (int i = 0; i < attempts; i++) {
        for (int i = 0; i < maxn; i++) {
            adj[i] = BITSET_INIT;
        }

        int n = randrange(core.size + 1, maxn);
        int ok = 1;
        graph_clear(g);

        // Copy core over
        for (int u = 0; u < core.size; u++)
            for (int v = u+1; v < core.size; v++) {
                int e = graph_get(&core, u, v);
                graph_set(g, u, v, e);
                adj[u] = bitset_set(adj[u], v, e != -1);
                adj[v] = bitset_set(adj[v], u, e != -1);
            }

        // Keep track of available nodes (those with allowed[u] != 0)
        bitset nodes = (((bitset) 1) << n) - 1;

        // For the existing core
        for (int u = 0; u < core.size; u++) {
            allowed[u] = delta - bitset_count(adj[u]);
            nodes = bitset_set(nodes, u, allowed[u] > 0);
        }

        // New nodes
        // don't need to update nodes here, since allowed > 0
        for (int u = core.size; u < n; u++)
            allowed[u] = randrange(1, delta - 1);

        // Link new nodes
        for (int u = core.size; u < n; u++) {
            if (allowed[u] == 0) continue;
            int core_count = randrange(1, allowed[u]); // # core nodes
            int m = allowed[u];

            for (int i = 0; i < m; i++) {
                int need_core = i < core_count;
                bitset peers = bitset_intersection(bitset_set(~adj[u], u, 0), nodes);

                // core_m = # peers available <= core.size
                int core_m = bitset_count(bitset_intersection(peers, core_adj));
                int min = need_core ? 0          : core_m;
                int max = need_core ? core_m - 1 : bitset_count(peers) - 1;
                if (min > max) continue;

                int v = bitset_nthset(peers, randrange(min, max));
                /* assert(v != -1 && allowed[v] != 0); */
                graph_set(g, u, v, 0);
                allowed[u]--;
                allowed[v]--;
                if (allowed[v] == 0)
                    nodes = bitset_set(nodes, v, 0);
                adj[u] = bitset_set(adj[u], v, 1);
                adj[v] = bitset_set(adj[v], u, 1);
            }

            if (allowed[u] == 0)
                nodes = bitset_set(nodes, u, 0);
        }

        // Check that it's valid!
        for (int u = 0; u < n; u++) {
            // For core nodes, degree needs to be delta
            // otherwise, degree needs to be in [1, delta-1] and needs to touch >= 1 core node
            int bs  = adj[u];
            int deg = bitset_count(bs);
            if ((u < core.size)
                    ? (deg != delta)
                    : (deg == 0 || deg == delta || !bitset_intersection(core_adj, bs))) {
                ok = 0;
                break;
            }
        }

        if (ok) return n;
    }
    return 0;
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
    char* buf = calloc(graph6_get_bytes_needed(nodes_per_semicore) + 1, sizeof(char));

    // Core extension
    int* allowed = calloc(nodes_per_semicore, sizeof(int));
    bitset* adj = calloc(nodes_per_semicore, sizeof(bitset));
    graph g = graph_create(nodes_per_semicore);

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        graph6_state gs = graph6_get_size(line);
        graph core = graph_create(gs.size);
        graph6_write_graph(line, gs.cursor, gs.size, &core);

        if (core.size + 1 < nodes_per_semicore) {
            for (int i = 0; i < semicores_per_core; i++) {
                int n = extend_core(core, nodes_per_semicore, delta, attempts, allowed, &g, adj);
                if (!n)
                    continue;
                int b = graph6_get_bytes_needed(n);

                // Verify that output is the same as showg
                /* for (int u = 0; u < n; u++) { */
                /*     for (int v = 0; v < n; v++) */
                /*         putchar(graph_get(&g, u, v) == 0 ? '1' : '0'); */
                /*     putchar('\n'); */
                /* } */

                memset(buf, 0, b);
                graph6_write_bytes(g, n, buf);
                buf[b] = '\n';

                write(1, buf, b+1);
            }
        }
        graph_free(&core);
    }

    graph_free(&g);
    free(allowed);
    free(adj);
}
