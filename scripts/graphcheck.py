# Check if a graph is a valid H_k
# E.g.
#  $ python scripts/geng.py ... | python scripts/graphcheck.py ... | ecol/ecol

import argparse
import sys
import json
from pyecol.graph import Graph


def is_valid_semicore(g: Graph, neighbours, core) -> bool:
    # Check that all nodes have a core-neighbour
    return all(neighbours[u] & core for u in g.nodes())


def is_valid_core(g: Graph, neighbours, core) -> bool:
    # Check that core is a disjoint union of cycles
    return all(len(neighbours[u] & core) <= 2 for u in core)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check that graphs belong in H_k')
    parser.add_argument('--delta', dest='delta', type=int, required=True)
    args = parser.parse_args()
    delta = args.delta

    for line in sys.stdin:
        u = json.loads(line)
        edge_data = u["edge_data"]
        g = Graph(len(edge_data))
        g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]

        deg = {u: g.degree(u) for u in g.nodes()}
        neighbours = {u: set(g.neighbours(u)) for u in g.nodes()}
        core = {u for u in g.nodes() if deg[u] == delta}
        if not core \
                or not min(deg.values()) == delta - 1 \
                or not max(deg.values()) == delta \
                or not is_valid_semicore(g, neighbours, core) \
                or not is_valid_core(g, neighbours, core):
            continue
        sys.stdout.write(line)
        sys.stdout.flush()
