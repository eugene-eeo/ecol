# Inteded usage:
#
#   $ python gen_nx.py | ecol/ecol > x.csv
#

import argparse
import itertools
import json
import sys

import networkx as nx
from pyecol.graph import Graph


def nx2graph(G: nx.Graph):
    g = Graph(len(G.nodes))
    for u, v in G.edges:
        g[u, v] = 0
    return g


def generate_graphs(delta, n, repeats=1000):
    r = [delta - 1, delta]
    for seq in itertools.product(r, repeat=n):
        if not nx.is_graphical(seq):
            continue
        for _ in range(repeats):
            try:
                yield nx2graph(nx.random_degree_sequence_graph(seq))
            except nx.NetworkXException:
                pass


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=True)
    parser.add_argument('--delta-core', dest='delta_core', type=int, required=True)
    parser.add_argument('--overfull', dest='underfull', action='store_false', required=False, default=True)

    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=20)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    delta = args.delta

    for n in range(args.start, args.end + 1, args.step):
        it = generate_graphs(
            delta=delta,
            n=n,
            underfull=args.underfull,
        )
        for g in it:
            data = {
                "n": n,
                "delta": delta,
                "edge_data": [[(-1 if x is False else x) for x in row]
                              for row in g.edge_data],
            }
            json.dump(data, sys.stdout)
            sys.stdout.write("\n")
            sys.stdout.flush()


if __name__ == '__main__':
    main()
