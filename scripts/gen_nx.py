# Inteded usage:
#
#   $ python gen_nx.py ... | python graphcheck.py ...
#

import argparse
import json
import sys
import random

import networkx as nx
from pyecol.graph import Graph
from pyecol.utils import is_overfull, graph_to_golang_graph


def nx2graph(G: nx.Graph):
    g = Graph(len(G.nodes))
    for u, v in G.edges:
        g[u, v] = 0
    return g


def generate_graphs(delta, n, repeats=1000, underfull=True):
    r = [delta - 1, delta]
    for _ in range(repeats):
        seq = [delta] + [random.choice(r) for _ in range(n-1)]
        if not nx.is_graphical(seq):
            continue
        try:
            g = nx2graph(nx.random_degree_sequence_graph(seq))
            if is_overfull(g) != underfull:
                yield g
        except nx.NetworkXUnfeasible:
            pass
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
    parser.add_argument('--repeats', dest='repeats', type=int, default=10000)

    args = parser.parse_args()
    delta = args.delta
    print("Parameters: start=%d, end=%d, repeats=%d, underfull=%r" % (args.start, args.end, args.repeats, args.underfull), file=sys.stderr)

    for n in range(args.start, args.end + 1, args.step):
        it = generate_graphs(
            delta=delta,
            n=n,
            underfull=args.underfull,
            repeats=args.repeats,
        )
        for g in it:
            data = {
                "n": g.n,
                "delta": delta,
                "edge_data": graph_to_golang_graph(g),
            }
            print(json.dumps(data))


if __name__ == '__main__':
    main()
