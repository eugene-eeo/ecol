import sys
import json
from pyecol.utils import golang_graph_to_graph, graph_to_golang_graph


def main():
    for line in sys.stdin:
        line = line.strip()
        data = json.loads(line)
        edge_data = data["edge_data"]

        g = golang_graph_to_graph(edge_data)
        deg = g.degrees()
        delta = max(deg.values())

        h = g.subgraph([u for u in g.nodes() if deg[u] == delta])
        data["edge_data"] = graph_to_golang_graph(h)

        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
