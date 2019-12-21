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


def run_command(n, delta, min_delta, underfull=True):
    template = 'geng -cq -d{min_delta} {n} | showg -a'
    mine = None
    maxe = None
    if delta is not None:
        # We cannot calculate a overfull/underfull mine/maxe without delta!
        template = 'geng -cq -d{min_delta} -D{delta} {n} {mine}:{maxe} | showg -a'
        if underfull:
            mine = 0
            maxe = delta * int(n // 2)
        else:
            mine = delta * int(n // 2) + 1
            maxe = 0

    cmd = template.format(
        mine=mine,
        maxe=maxe,
        min_delta=min_delta,
        delta=delta,
        n=n,
    )
    print(cmd, file=sys.stderr)
    proc = subprocess.Popen(
        cmd,
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


def adj_mat_to_graph(lines, n, underfull=None):
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
            if underfull is None or is_overfull(g) == (not underfull):
                yield g


def generate_graphs(args):
    if args.min_delta is None:
        args.min_delta = args.delta - 1 if (args.delta is not None) else 1
    for n in range(args.start, args.end + 1, args.step):
        yield from adj_mat_to_graph(
            run_command(n=n, delta=args.delta, min_delta=args.min_delta, underfull=args.underfull),
            n=n,
            underfull=args.underfull,
        )


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=False, default=None)
    parser.add_argument('--min-delta', dest='min_delta', type=int, required=False, default=None)

    parser.add_argument('--underfull', dest='underfull', action='store_true', required=False, default=None)
    parser.add_argument('--overfull', dest='underfull', action='store_false', required=False)

    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=13)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    for g in generate_graphs(args):
        data = {
            "n": g.n,
            "delta": max(g.degrees().values()),
            "edge_data": [[(-1 if x is False else x) for x in row]
                          for row in g.edge_data],
        }
        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
