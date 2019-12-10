import sys
import json
from pyecol.graph import Graph


def main():
    for line in sys.stdin:
        data = json.loads(line)
        edge_data = data["edge_data"]
        g = Graph(len(edge_data))
        g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]

        deg = g.degrees()
        delta = max(deg.values())

        h = g.subgraph([u for u in g.nodes() if deg[u] == delta])
        data["edge_data"] = [[(-1 if x is False else x) for x in row] for row in h.edge_data]

        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
