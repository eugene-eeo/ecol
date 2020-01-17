# needs pyenv shell 2.7.17 since pynauty is installed there!

import sys
import json
from collections import deque
from pynauty import Graph, isomorphic


def get_adj_dict(edge_data):
    d = {}
    n = len(edge_data)
    for i, row in enumerate(edge_data):
        d[i] = [j for j in range(i + 1, n) if row[j] == 0]
    return d


def cvt_graph(edge_data):
    return Graph(len(edge_data), directed=False, adjacency_dict=get_adj_dict(edge_data))


def filter_isomorphic(graphs):
    MAX = 5000
    prevs = deque(maxlen=MAX)
    for line, graph in graphs:
        if any(isomorphic(graph, g) for g in prevs):
            continue
        prevs.append(graph)
        yield line


def graphs_from_stdin():
    for i, line in enumerate(sys.stdin):
        data = json.loads(line.strip())
        yield line, cvt_graph(data["edge_data"])
        if i % 100 == 0:
            sys.stderr.write("%d\n" % i)
            sys.stderr.flush()


if __name__ == '__main__':
    for line in filter_isomorphic(graphs_from_stdin()):
        sys.stdout.write(line)
