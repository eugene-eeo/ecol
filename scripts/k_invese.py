import json
import sys
from pyecol.graph import Graph
from pyecol.utils import max_degree


def gen(m):
    g = Graph(2 * m + 1)
    for u in range(m):
        for v in range(m, g.n):
            g[u, v] = 0

    for i in range(m + 1):
        u = m + i
        v = m + ((i + 1) % (m + 1))
        g[u, v] = 0
    return g


if __name__ == '__main__':
    for n in range(2, 10):
        g = gen(n)
        delta = max_degree(g)
        data = {
            "n": g.n,
            "delta": delta,
            "edge_data": [[(-1 if x is False else x) for x in row]
                          for row in g.edge_data],
        }
        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()
