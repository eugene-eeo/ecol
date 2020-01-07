import sys
import json
import networkx as nx
from collections import deque
from pyecol.utils import golang_graph_to_graph


def golang_graph2graph(edge_data) -> nx.Graph:
    g = golang_graph_to_graph(edge_data)
    G = nx.Graph()
    G.add_edges_from(g.edges())
    return G


def filter_isomorphic(graphs):
    MAX = 2000
    prevs = deque(maxlen=MAX)
    for data, graph in graphs:
        # otherwise perform checks
        found = any(
            nx.fast_could_be_isomorphic(graph, g) and nx.is_isomorphic(graph, g)
            for g in prevs
        )
        if found:
            continue
        if len(prevs) == MAX:
            prevs.popleft()
        prevs.append(graph)
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
