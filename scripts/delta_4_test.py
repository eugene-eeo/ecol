# Inteded usage:
#
#   $ python delta_4_test.py | ecol/ecol > x.csv
#

import itertools
import argparse
import json
import random
import sys
from pyecol.graph import Graph
from pyecol.utils import is_overfull


def generate_base_graph(n: int, delta: int) -> (Graph, dict):
    g = Graph(n)
    deg = {u: 0 for u in range(n)}
    for u, row in enumerate(g.edge_data):
        if deg[u] == delta:
            continue
        peers = {v for v, d in deg.items()
                 if d < delta and row[v] is False and v != u}
        num_peers = min(len(peers), delta - deg[u])
        if num_peers > 0:
            peers = random.sample(peers, random.randint(0, num_peers))
            for v in peers:
                g[u, v] = 0
                deg[u] += 1
                deg[v] += 1
    return g, deg


def is_semicore(G: Graph, core: set):
    # Check if a graph is a valid semicore (all nodes are connected to
    # a core node)
    for u in set(G.nodes()) - core:
        if not core & set(G.neighbours(u)):
            return False
    return True


def generate_graph(n: int, delta: int = 4, attempts: int = 100, delta_core=2, checks=[]) -> Graph:
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
                or core_max_degree > delta_core \
                or is_overfull(g) \
                or not all(f(g, core) for f in checks) \
                or not is_semicore(g, core):
            continue
        return g
    return None


def core_is_complete(g: Graph, core: set):
    '''Check if the graph core is complete'''
    for u in core:
        for v in core:
            if u != v and g.edge_data[u][v] is False:
                return False
    return True


def contains_k5e(g: Graph, core: set):
    '''Check if the graph contains K_5 - e as a subgraph'''
    neighbours = {u: set(g.neighbours(u)) for u in range(g.n)}
    candidates = [u for u in neighbours if len(neighbours[u]) >= 3]
    for subset in itertools.combinations(candidates, 5):
        subset = set(subset)
        degs = [len(neighbours[u] & subset) for u in subset]
        degs.sort()
        if degs == [3, 3, 4, 4, 4]:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=True)
    parser.add_argument('--delta-core', dest='delta_core', type=int, required=True)

    parser.add_argument('--repeats', dest='repeats', type=int, default=1000)
    parser.add_argument('--attempts', dest='attempts', type=int, default=1000)
    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=20)
    parser.add_argument('--step', dest='step', type=int, default=1)

    # Checks
    parser.add_argument('--contains-k5e', dest='contains_k5e', action='store_true', default=False)
    parser.add_argument('--complete-core', dest='complete_core', action='store_true', default=False)

    args = parser.parse_args()
    delta = args.delta

    checks = []
    if args.contains_k5e:
        checks.append(contains_k5e)
    if args.complete_core:
        checks.append(core_is_complete)

    for n in range(args.start, args.end + 1, args.step):
        for i in range(args.repeats):
            g = generate_graph(
                n, delta=delta,
                attempts=args.attempts,
                checks=checks,
                delta_core=args.delta_core,
            )
            # sys.stderr.write(f"[{n}] {i} ok={g is not None}\n")
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
            sys.stdout.flush()


if __name__ == '__main__':
    main()
