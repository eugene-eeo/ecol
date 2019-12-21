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

    return G


def main():
    cores = defaultdict(list)
    for i, line in enumerate(open(sys.argv[1])):
        z = json.loads(line)
        g = golang_graph2graph(z["edge_data"])
        cores[g.n].append(g)

    for n in sorted(cores)[1:]:
        for g in cores[n]:
            print(any(subgraph_isomorphism(
                sub=sub,
                g=g,
                max_n=1,
                induced=True,
            ) for sub in cores[n-1]))


if __name__ == '__main__':
    main()
