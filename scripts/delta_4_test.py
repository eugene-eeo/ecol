# Inteded usage:
#
#   $ python delta_4_test.py | ecol/ecol > x.csv
#

import argparse
import json
import random
import sys
from pyecol.graph import Graph
from pyecol.utils import is_overfull


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


def is_connected(G: Graph, core: set):
    for u in set(G.nodes()) - core:
        if not core & set(G.neighbours(u)):
            return False
    return True


def generate_graph(n: int, delta: int = 4, attempts: int = 100) -> Graph:
    # Core has delta <= 2
    # G has delta <= 4
    # n = total # of vertices
    while attempts > 0:
        attempts -= 1
        g, deg = generate_base_graph(n, delta)
        g_delta = max(deg.values())
        core = {u for u in g.nodes() if deg[u] == g_delta}
        core_max_degree = max(
            sum(1 for v in g.neighbours(u) if v in core)
            for u in core
        )
        if g_delta != delta \
                or core_max_degree > 2 \
                or is_overfull(g) \
                or not is_connected(g, core):
            continue
        return g
    return None


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded delta and core with max degree 2.')
    parser.add_argument('--delta', dest='delta', type=int, default=4)
    parser.add_argument('--repeats', dest='repeats', type=int, default=1000)
    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=100)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    delta = args.delta

    for n in range(args.start, args.end, args.step):
        for _ in range(args.repeats):
            g = generate_graph(n, delta=delta, attempts=100)
            if g is None:
                continue
            data = {
                "n": n,
                "class": 1,
                "delta": delta,
                "edge_data": [[(-1 if x is False else x) for x in row]
                              for row in g.edge_data],
            }
            json.dump(data, sys.stdout)
            sys.stdout.write("\n")


if __name__ == '__main__':
    main()
