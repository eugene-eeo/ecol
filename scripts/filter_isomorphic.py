import sys
import json
import networkx as nx
from pyecol.graph import Graph


def golang_graph2graph(edge_data) -> nx.Graph:
    g = Graph(len(edge_data))
    g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]
    G = nx.Graph()
    G.add_edges_from(g.edges())
    return G


def filter_isomorphic(graphs):
    prev = None
    for data, graph in graphs:
        # otherwise perform checks
        if (prev is not None
                and nx.fast_could_be_isomorphic(graph, prev)
                and nx.is_isomorphic(graph, prev)):
            continue
        prev = graph
        yield data


def graphs_from_stdin():
    for line in sys.stdin:
        data = json.loads(line.strip())
        yield data, golang_graph2graph(data["edge_data"])


if __name__ == '__main__':
    for data in filter_isomorphic(graphs_from_stdin()):
        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()
