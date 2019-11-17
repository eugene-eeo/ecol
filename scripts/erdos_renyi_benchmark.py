import csv
import sys
from collections import defaultdict


def main():
    f = csv.reader(sys.stdin)
    next(f)
    vh = defaultdict(int)
    cg = defaultdict(int)
    counts = defaultdict(int)
    for row in f:
        n, p, delta, vh_c, cg_c = row
        counts[n, p] += 1
        if delta == cg_c: cg[n, p] += 1  # noqa: E701
        if delta == vh_c: vh[n, p] += 1  # noqa: E701

    w = csv.writer(sys.stdout)
    w.writerow(['n', 'p', 'vh', 'cg'])
    for n, p in sorted(counts, key=lambda x: (x[1], int(x[0]))):
        N = counts[n, p]
        w.writerow([n, p, vh[n, p]/N, cg[n, p]/N])


if __name__ == '__main__':
    main()
