import csv
import sys


def main():
    f = csv.reader(sys.stdin)
    next(f)
    ones = {}
    for row in f:
        n, m, delta, colours = row
        ones[int(n), int(m)] = delta == colours

    w = csv.writer(sys.stdout)
    w.writerow(['n', 'm', 'class_one'])
    for n, m in sorted(ones):
        w.writerow([n, m, ones[n, m]])


if __name__ == '__main__':
    main()
