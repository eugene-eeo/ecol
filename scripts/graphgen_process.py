import pprint
import json
import sys
from pyecol.graph import Graph
from pyecol.utils import plot_graph


def main():
    for line in open(sys.argv[1]):
        z = json.loads(line)
        # if z["n"] < 30:
        #     continue
        c = dict(z)
        del c["edge_data"]
        pprint.pprint(c)
        if input("display? ").strip().lower() == "y":
            g = Graph(len(z["edge_data"]))
            g.edge_data = [[(x if x != -1 else False) for x in row] for row in z["edge_data"]]
            plot_graph(g, with_labels=True).render(view=True)


if __name__ == '__main__':
    main()
