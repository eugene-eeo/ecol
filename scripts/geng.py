# Inteded usage:
#
#   $ python geng.py | ecol/ecol
#

import argparse
import json
import sys
import subprocess

from pyecol.graph import Graph
from pyecol.utils import is_overfull, graph_to_golang_graph, max_degree


def run_command(n, delta, min_delta, underfull):
    template = 'geng -c -d{min_delta} {n} | showg -a'
    mine = None
    maxe = None
    if delta is not None:
        if underfull is not None:
            # We cannot calculate a overfull/underfull mine/maxe without delta!
            template = 'geng -c -d{min_delta} -D{delta} {n} {mine}:{maxe} | showg -a'
            if underfull:
                mine = 0
                maxe = delta * int(n // 2)
            else:
                mine = delta * int(n // 2) + 1
                maxe = 0
        else:
            template = 'geng -c -d{min_delta} -D{delta} {n} {mine}:0 | showg -a'
            mine = max(delta, n - 1)

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
        stderr=sys.stderr,
    )
    while True:
        line = proc.stdout.readline()
        if line == b"" and proc.poll() is not None:
            break
        yield line.decode('ascii')


def deg_core(g):
    deg = g.degrees()
    delta = max(deg.values())
    h = g.subgraph([n for n, d in deg.items() if d == delta])
    return max_degree(h)


def graph_is_semicore(g):
    deg = g.degrees()
    delta = max(deg.values())
    core = [n for n, d in deg.items() if d == delta]
    ed = g.edge_data
    for i, d in deg.items():
        row = ed[i]
        if d != delta and not any(row[u] is not False for u in core):
            return False
    return True


def adj_mat_to_graph(lines, n, delta=None, underfull=None, delta_core=None, is_semicore=False):
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
            if (delta is None or max_degree(g) == delta) and \
                    (underfull is None or is_overfull(g) == (not underfull)) and \
                    (delta_core is None or deg_core(g) == delta_core) and \
                    (not is_semicore or graph_is_semicore(g)):
                yield g


def generate_graphs(args):
    for n in range(args.start, args.end + 1, args.step):
        yield from adj_mat_to_graph(
            run_command(n=n, delta=args.delta, min_delta=args.min_delta, underfull=args.underfull),
            n=n,
            delta=args.delta,
            underfull=args.underfull,
            delta_core=args.delta_core,
            is_semicore=args.is_semicore,
        )


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=False, default=None)
    parser.add_argument('--min-delta', dest='min_delta', type=int, required=False, default=None)
    parser.add_argument('--delta-core', dest='delta_core', type=int, required=False, default=None)
    parser.add_argument('--is-semicore', dest='is_semicore', action='store_true', required=False, default=False)

    parser.add_argument('--underfull', dest='underfull', action='store_true', required=False, default=None)
    parser.add_argument('--overfull', dest='underfull', action='store_false', required=False, default=None)

    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=13)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    if args.min_delta is None:
        args.min_delta = 1

    print(args, file=sys.stderr)
    for g in generate_graphs(args):
        data = {
            "n": g.n,
            "delta": max(g.degrees().values()),
            "edge_data": graph_to_golang_graph(g),
        }
        json.dump(data, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
