import csv
import sys
from collections import defaultdict


def main():
    f = csv.reader(sys.stdin)
    next(f)
    class_one = defaultdict(int)
    counts = defaultdict(int)
    for row in f:
        n, p, delta, colours = row
        counts[n, p] += 1
        if delta == colours:
            class_one[n, p] += 1

    w = csv.writer(sys.stdout)
    w.writerow(['n', 'p', 'prob'])
    for n, p in sorted(counts, key=lambda x: (x[1], int(x[0]))):
        w.writerow([n, p, class_one[n, p] / float(counts[n, p])])


if __name__ == '__main__':
    main()
