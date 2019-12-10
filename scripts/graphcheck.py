# Check if a graph is a valid H_k
# E.g.
#  $ python scripts/geng.py ... | python scripts/graphcheck.py | ecol/ecol

import sys
import json
import argparse
from pyecol.graph import Graph


def is_valid_semicore(g: Graph, neighbours, core) -> bool:
    # Check that all nodes have a core-neighbour
    return all(neighbours[u] & core for u in g.nodes())


def is_valid_core(g: Graph, neighbours, core) -> bool:
    # Check that core is a disjoint union of cycles
    return all(len(neighbours[u] & core) <= 2 for u in core)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--relax-core', dest='relax_core', default=False, action='store_true')

    args = parser.parse_args()

    for line in sys.stdin:
        u = json.loads(line)
        edge_data = u["edge_data"]
        g = Graph(len(edge_data))
        g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]

        deg = g.degrees()
        delta = max(deg.values())
        neighbours = {u: set(g.neighbours(u)) for u in g.nodes()}
        core = {u for u in g.nodes() if deg[u] == delta}
        if core \
                and min(deg.values()) == delta - 1 \
                and is_valid_semicore(g, neighbours, core) \
                and (args.relax_core or is_valid_core(g, neighbours, core)):
            sys.stdout.write(line)
            sys.stdout.flush()
