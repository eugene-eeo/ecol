import sys
import ujson as json
from graph_tool import Graph
from graph_tool.topology import subgraph_isomorphism
from pyecol.graph import Graph as PyecolGraph


def golang_graph_to_graph(edge_data):
    g = PyecolGraph(len(edge_data))
    g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]
    return g


def golang_graph_to_graphtool_graph(edge_data):
    g = golang_graph_to_graph(edge_data)
    G = Graph(directed=False)
    handles = [G.add_vertex() for _ in g.nodes()]
    for u, v in g.edges():
        G.add_edge(handles[u], handles[v])
    return G


def check_claim(graphs, n, g):
    for m in range(n - 1, 3, -1):
        for _, h in graphs.get(m, []):
            if subgraph_isomorphism(h, g, max_n=1, induced=True):
                return m
    return None


def main():
    graphs = {}
    for i, line in enumerate(sys.stdin):
        line = line.strip()
        data = json.loads(line)
        edge_data = data["edge_data"]
        n = len(edge_data)
        if n not in graphs:
            graphs[n] = []
        graphs[n].append((line, golang_graph_to_graphtool_graph(edge_data)))
        if i % 100 == 0:
            print(i, file=sys.stderr)

    print("done loading", file=sys.stderr)

    for i, n in enumerate(graphs):
        print(i, file=sys.stderr)
        for line, g in graphs[n]:
            x = check_claim(graphs, n, g)
            # print(n, x, file=sys.stderr)
            if x is None:
                print(line)


if __name__ == '__main__':
    main()
