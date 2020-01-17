import sys
import json
from collections import deque

from graph_tool import Graph
from graph_tool.topology import isomorphism


def get_edge_list(edge_data):
    n = len(edge_data)
    for i, row in enumerate(edge_data):
        for j in range(i + 1, n):
            if row[j] == 0:
                yield (i, j)


def golang_graph_to_graphtool_graph(edge_data):
    G = Graph(directed=False)
    G.add_vertex(n=len(edge_data))
    G.add_edge_list(get_edge_list(edge_data))
    return G


def filter_isomorphic(graphs):
    MAX = 1000
    prevs = deque(maxlen=MAX)
    for line, graph in graphs:
        if any(isomorphism(graph, g) for g in prevs):
            continue
        prevs.append(graph)
        yield line


def graphs_from_stdin():
    for i, line in enumerate(sys.stdin):
        data = json.loads(line.strip())
        yield line, golang_graph_to_graphtool_graph(data["edge_data"])
        if i % 100 == 0:
            sys.stderr.write("%d\n" % i)
            sys.stderr.flush()


if __name__ == '__main__':
    for line in filter_isomorphic(graphs_from_stdin()):
        sys.stdout.write(line)
