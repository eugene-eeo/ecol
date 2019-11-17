# Inteded usage:
#
#   $ python delta_4_test.py | ecol/ecol > x.csv
#

import sys
import random
import json
from pyecol.graph import Graph
from pyecol.utils import max_degree


def is_overfull(g: Graph) -> bool:
    return g.num_edges() > max_degree(g) * (g.n // 2)


def generate_base_graph(n: int, delta: int) -> (Graph, dict):
    g = Graph(n)
    deg = {u: 0 for u in range(n)}
    for u in range(n):
        if deg[u] == delta:
            continue
        peers = {v for v in range(n)
                 if deg[v] < delta and g.edge_data[u][v] is False and v != u}
        num_peers = min(len(peers), delta - deg[u])
        if num_peers > 0:
            peers = random.sample(peers, random.randint(0, num_peers))
            for v in peers:
                g[u, v] = 0
                deg[u] += 1
                deg[v] += 1
    return g, deg


def generate_graph(n: int, delta: int = 4, attempts: int = 100) -> Graph:
    # Core has delta <= 2
    # G has delta <= 4
    # n = total # of vertices
    while attempts > 0:
        attempts -= 1
        g, deg = generate_base_graph(n, delta)
        delta = max(deg.values())
        core = {u for u in g.nodes() if deg[u] == delta}
        core_max_degree = max(
            sum(1 for v in g.neighbours(u) if v in core)
            for u in core
        )
        if core_max_degree > 2:
            continue
        return g
    return None


def main():
    for delta in [3, 4]:
        for n in range(5, 100):
            for _ in range(1000):
                g = generate_graph(n, delta=delta, attempts=100)
                if g is None or is_overfull(g):
                    continue
                data = {
                    "n": n,
                    "class": 1,
                    "delta": max_degree(g),
                    "edge_data": [[(-1 if x is False else x) for x in row]
                                  for row in g.edge_data],
                }
                json.dump(data, sys.stdout)
                sys.stdout.write("\n")


if __name__ == '__main__':
    main()
