# Inteded usage:
#
#   $ python geng_raw.py | ecol/ecol -gc
#

import os
import argparse
import sys


def run_command(n, delta, min_delta, underfull):
    template = 'geng -c -d{min_delta} {n}'
    mine = None
    maxe = None
    if delta is not None:
        if underfull is not None:
            # We cannot calculate a overfull/underfull mine/maxe without delta!
            template = 'geng -c -d{min_delta} -D{delta} {n} {mine}:{maxe}'
            if underfull:
                mine = 0
                maxe = delta * int(n // 2)
            else:
                mine = delta * int(n // 2) + 1
                maxe = 0
        else:
            template = 'geng -c -d{min_delta} -D{delta} {n} {mine}:0'
            mine = max(delta, n - 1)

    cmd = template.format(
        mine=mine,
        maxe=maxe,
        min_delta=min_delta,
        delta=delta,
        n=n,
    )
    print(cmd, file=sys.stderr)
    os.system(cmd)


def generate_graphs(args):
    for n in range(args.start, args.end + 1, args.step):
        run_command(n=n, delta=args.delta, min_delta=args.min_delta, underfull=args.underfull)


def main():
    parser = argparse.ArgumentParser(description='Generate graphs with bounded overall and core delta.')
    parser.add_argument('--delta', dest='delta', type=int, required=False, default=None)
    parser.add_argument('--min-delta', dest='min_delta', type=int, required=False, default=None)

    parser.add_argument('--underfull', dest='underfull', action='store_true', required=False, default=None)
    parser.add_argument('--overfull', dest='underfull', action='store_false', required=False, default=None)

    parser.add_argument('--start', dest='start', type=int, default=5)
    parser.add_argument('--end', dest='end', type=int, default=13)
    parser.add_argument('--step', dest='step', type=int, default=1)

    args = parser.parse_args()
    if args.min_delta is None:
        args.min_delta = 1

    print(args, file=sys.stderr)
    os.environ['PATH'] += os.pathsep + '/home/eeojun/Downloads/nauty26r12/'
    generate_graphs(args)


if __name__ == '__main__':
    main()
