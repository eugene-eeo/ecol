import csv
import sys
from itertools import repeat, chain
from multiprocessing import Pool
from heuristic import vizing_heuristic
from utils import ColouringGraph, colours_used, max_degree
from graph import erdos_renyi_graph


def job(params):
    n, p = params
    g = ColouringGraph.wrap(erdos_renyi_graph(n, p))
    vizing_heuristic(g)
    return n, p, max_degree(g), colours_used(g)


def main():
    f = csv.writer(sys.stdout)
    f.writerow(['n', 'p', 'delta', 'colours_used'])
    params = chain.from_iterable(
        repeat((n, p), 5000)
        for n in range(1, 200, 5)
        for p in [0.125, 0.25, 0.5, 0.75, 0.95]
    )
    with Pool(processes=8) as pool:
        for n, p, delta, colours in pool.imap(job, params):
            f.writerow([n, p, delta, colours])


if __name__ == '__main__':
    main()
