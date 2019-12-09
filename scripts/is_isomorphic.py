import sys
import json
import networkx as nx
from pyecol.graph import Graph


def main():
    base = None

    for i, line in enumerate(open(sys.argv[1])):
        z = json.loads(line)
        edge_data = z["edge_data"]
        g = Graph(len(edge_data))
        g.edge_data = [[(False if x == -1 else x) for x in row] for row in edge_data]

        G = nx.DiGraph()
        G.add_edges_from(list(g.edges()))
        print([y for x, y in sorted(G.degree, key=lambda x: x[1])])

        if not base:
            base = G
        else:
            print(nx.is_isomorphic(base, G))


if __name__ == '__main__':
    main()
