# check_is.py
#
# Needs to be ran in the root directory on system python3 with
# graph_tool installed (since there is no graph_tool on pip...).


from bisect import bisect_left
from collections import defaultdict
import json
import sys

import graph_tool as gt
from graph_tool.topology import subgraph_isomorphism

from pyecol.graph import Graph


def golang_graph2graph(edge_data) -> gt.Graph:
    g = Graph(len(edge_data))
    g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]

    G = gt.Graph(directed=False)
    v = [G.add_vertex() for _ in range(g.n)]
    for i, j in g.edges():
        G.add_edge(v[i], v[j])

    return g, G


def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1


def is_sublist(a, b):
    first_index = index(b, a[0])
    if first_index == -1:
        return False
    n = len(a)
    for i in range(first_index, len(b) - 1):
        if a == b[i:i+n]:
            return True
    return False


def check_degseq(g, G, degseq, cores):
    for m in range(min(cores), g.n):
        for _, _, degs in cores[m]:
            if is_sublist(degs, degseq):
                return True
    return False


def check_induced(g, G, degseq, cores):
    for m in range(min(cores), g.n):
        for _, sub, _ in cores[m]:
            if subgraph_isomorphism(sub=sub, g=G, max_n=1, induced=True):
                return True
    return False


def main():
    cores = defaultdict(list)
    for i, line in enumerate(open(sys.argv[1])):
        z = json.loads(line)
        g, G = golang_graph2graph(z["edge_data"])
        cores[g.n].append((g, G, sorted(g.degrees().values())))

    for n in sorted(cores)[1:]:
        for i, (g, G, degseq) in enumerate(cores[n], 1):
            if not check_induced(g, G, degseq, cores):
                # print(n, i, file=sys.stderr)
                edge_data = [[-1 if x is False else x for x in row] for row in g.edge_data]
                data = {
                    "n": g.n,
                    "edge_data": edge_data,
                }
                json.dump(data, sys.stdout)
                sys.stdout.write("\n")


if __name__ == '__main__':
    main()
