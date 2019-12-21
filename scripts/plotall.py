import json
import sys
from pyecol.graph import Graph
from pyecol.utils import plot_graph


def main():
    for i, line in enumerate(open(sys.argv[1])):
        z = json.loads(line)
        g = Graph(len(z["edge_data"]))

        # if g.n != 8:
        #     continue

        g.edge_data = [[(x if x != -1 else False) for x in row] for row in z["edge_data"]]
        seq = list(g.degrees().values())
        seq.sort()

        # if seq != [g.n - 1] * g.n:
        #     continue

        plot_graph(g, with_labels=False).render(
            filename=f"r2/{sys.argv[1]}.{g.n}.{i}",
            cleanup=True,
        )


if __name__ == '__main__':
    main()
