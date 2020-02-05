# produce_graphs
# ==============
#
# produce graphs which have all possible edge deletions

import argparse
import sys
import json
from itertools import combinations, chain
from pyecol.graph import Graph
from pyecol.utils import graph_to_golang_graph


def construct(n, k):
    assert n % 2 == 0
    g = Graph(n + 4)

    # make complete graph on n vertices
    for i in range(n):
        for j in range(i + 1, n):
            g[i, j] = 0

    edges = []

    # add the 1 vertex
    g[0, n] = 0
    edges.append((0, n))

    # add the n+1 and n+2 vertices
    for i in range(n):
        g[i, n + 1] = 0
        g[i, n + 2] = 0
        edges.extend([
            (i, n+1),
            (i, n+2),
        ])

    # add the n+3 vertex
    g[n + 1, n + 3] = 0
    g[n + 2, n + 3] = 0
    edges.extend([
        (n+1, n+3),
        (n+2, n+3),
    ])
    for i in range(1, n):
        g[i, n + 3] = 0
        edges.append((i, n+3))

    for to_delete in chain.from_iterable(combinations(edges, i) for i in range(1, k+1)):
        for u, v in to_delete:
            del g[u, v]

        deg = g.degrees()
        delta = max(deg.values())
        valid = True
        for node, d in deg.items():
            valid = (d == delta if 0 <= node < n else
                     d < delta)
            if not valid:
                break
        if valid:
            yield g

        for u, v in to_delete:
            g[u, v] = 0

    return g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=4)
    parser.add_argument("--end", type=int, default=30)
    parser.add_argument("--k", type=int, default=2)
    opt = parser.parse_args()

    for n in range(opt.start, opt.end + 2, 2):
        print("[n=%d]" % n, file=sys.stderr)
        for g in construct(n, k=opt.k):
            print(json.dumps({
                "n": n,
                "edge_data": graph_to_golang_graph(g),
            }))


if __name__ == '__main__':
    main()
