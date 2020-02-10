# cc_gen.py
# =========
# Generate G around H(n) = Cn * C(n-1)

import json
from pyecol.graph import Graph
from pyecol.utils import graph_to_golang_graph


def construct(n):
    g = Graph(n + n - 1 + 3)
    # generate core

    # first cycle Cn
    for u in range(1, n):
        g[u-1, u] = 0
    g[0, n-1] = 0

    # second cycle Cn-1
    for u in range(n + 1, n + n - 1):
        g[u-1, u] = 0
    g[n, n + (n - 1) - 1] = 0

    # join cycles
    for u in range(n):
        for v in range(n, n + n - 1):
            g[u, v] = 0

    # add extension nodes
    for u in range(0, n):
        g[n+n-1, u] = 0
    for u in range(0, n + n - 1):
        g[n+n+0, u] = 0
        g[n+n+1, u] = 0

    return g


def main():
    for n in range(4, 10):
        print(json.dumps({
            "n": n,
            "edge_data": graph_to_golang_graph(construct(n)),
        }))


if __name__ == '__main__':
    main()
