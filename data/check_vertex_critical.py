# check_vertex_critical
# =====================
#
# check if the graph family we produce in check_claim is edge critical

import sys
import json
from pyecol.graph import Graph
from pyecol.utils import graph_to_golang_graph


def construct(n):
    assert n % 2 == 0
    g = Graph(n + 2)

    # Make complete graph on n vertices
    for i in range(n):
        for j in range(i + 1, n):
            g[i, j] = 0

    # Add the 1 vertex
    g[0, n] = 0

    # Add the n+1 and n+2 vertices
    for i in range(n):
        g[i, n + 1] = 0
        g[i, n + 2] = 0

    # Add the n+3 vertex
    # g[n + 1, n + 3] = 0
    # g[n + 2, n + 3] = 0
    for i in range(1, n):
        g[i, n + 3] = 0

    return g


def main():
    for n in range(4, 100, 2):
        print(n, file=sys.stderr)
        print(json.dumps({
            "n": n,
            "edge_data": graph_to_golang_graph(construct(n)),
        }))


if __name__ == '__main__':
    main()
