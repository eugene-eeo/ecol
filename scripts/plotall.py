import json
import argparse
from pyecol.graph import Graph
from pyecol.utils import plot_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('-d', '--dir', type=str, default='.', required=False)
    parser.add_argument('-p', '--prefix', type=str, default=None, required=False)

    args = parser.parse_args()
    args.prefix = args.file if args.prefix is None else args.prefix

    for i, line in enumerate(open(args.file)):
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
            filename=f"{args.dir}/{args.prefix}.{g.n}.{i}",
            cleanup=True,
        )


if __name__ == '__main__':
    main()
