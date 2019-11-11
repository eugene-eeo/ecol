import pprint
import json
import sys
from graph import Graph
from utils import plot_graph


def main():
    for line in open(sys.argv[1]):
        z = json.loads(line)
        # if z["is_class_one"]:
        #     continue
        pprint.pprint({
            "k": z["k"],
            "n": z["n"],
            "class_one": z["is_class_one"],
        })
        if input("display? ").strip().lower() == "y":
            g = Graph(z["k"] + z["n"])
            g.edge_data = [[(x if x != -1 else False) for x in row] for row in z["edge_data"]]
            plot_graph(g, with_labels=False).render(view=True)


if __name__ == '__main__':
    main()
