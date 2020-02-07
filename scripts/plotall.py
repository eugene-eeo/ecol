import json
import argparse
from pyecol.graph import Graph
from pyecol.utils import plot_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('-d', '--dir', type=str, default='.', required=False)
    parser.add_argument('-p', '--prefix', type=str, default=None, required=False)
    parser.add_argument('--node-label', dest='node_label', type=str, default="node_num", required=False)
    parser.add_argument('--no-core-same-rank', dest='core_same_rank', action='store_false')
    parser.add_argument('--nice-core', dest='nice_core', action='store_true')
    parser.set_defaults(core_same_rank=True)

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

        plot_graph(
            g,
            with_labels=False,
            node_label=args.node_label,
            core_same_rank=args.core_same_rank,
            nice_core=args.nice_core,
        ).render(
            filename=f"{args.dir}/{args.prefix}.{g.n}.{i}",
            cleanup=True,
        )


if __name__ == '__main__':
    main()
