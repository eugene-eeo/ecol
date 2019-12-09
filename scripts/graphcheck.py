# Check if a graph is a valid H_k
# E.g.
#  $ python scripts/geng.py ... | python scripts/graphcheck.py ... | ecol/ecol

import argparse
import sys
import json
from pyecol.graph import Graph


def is_valid_semicore(g: Graph, core) -> bool:
    # Check that all nodes have a core-neighbour
    for u in g.nodes():
        if not set(g.neighbours(u)) & core:
            return False
    return True


def is_valid_core(g: Graph, core) -> bool:
    # Check that core is a disjoint union of cycles
    for u in core:
        if len(set(g.neighbours(u)) & core) != 2:
            return False
    return True


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
        core = {u for u in g.nodes() if deg[u] == delta}
        if not core \
                or not min(deg.values()) == delta - 1 \
                or not max(deg.values()) == delta \
                or not is_valid_semicore(g, core) \
                or not is_valid_core(g, core):
            continue
        sys.stdout.write(line)
        sys.stdout.flush()
