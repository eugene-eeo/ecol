# Inteded usage:
#
#   $ python geng.py | ecol/ecol
#

import argparse
import json
import sys
import subprocess

from pyecol.graph import Graph
from pyecol.utils import is_overfull


def run_command(n, delta, underfull=True):
    if underfull:
        mine = 0
        maxe = delta * int(n // 2)
    else:
        mine = delta * int(n // 2) + 1
        maxe = 0

    print(f'geng -cq -d{delta-1} -D{delta} {n} {mine}:{maxe}', file=sys.stderr)
    proc = subprocess.Popen(
        f'geng -cq -d{delta-1} -D{delta} {n} {mine}:{maxe} | showg -a',
        shell=True,
        env={"PATH": "/home/eeojun/Downloads/nauty26r12/"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    while True:
        line = proc.stdout.readline()
        if line == b"" and proc.poll() is not None:
            break
        yield line.decode('ascii')


def adj_mat_to_graph(lines, n, underfull=False):
    while True:
        line = next(lines, "")
        if not line:
            break

        if line.startswith("Graph"):
            mat = []
            for _, line in zip(range(n), lines):
                mat.append(line.strip())
            g = Graph(n)
            g.edge_data = [[False if x == '0' else 0 for x in row] for row in mat]
            if is_overfull(g) != underfull:
                yield g


def generate_graphs(delta, n, **kwargs):
    return adj_mat_to_graph(run_command(n, delta, **kwargs), n, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=True)
    parser.add_argument('--overfull', dest='underfull', action='store_false', required=False, default=True)

    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=20)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    delta = args.delta

    for n in range(args.start, args.end + 1, args.step):
        it = generate_graphs(
            delta=delta,
            n=n,
            underfull=args.underfull,
        )
        for g in it:
            data = {
                "n": n,
                "delta": delta,
                "edge_data": [[(-1 if x is False else x) for x in row]
                              for row in g.edge_data],
            }
            json.dump(data, sys.stdout)
            sys.stdout.write("\n")
            sys.stdout.flush()


if __name__ == '__main__':
    main()
