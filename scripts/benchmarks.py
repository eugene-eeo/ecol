import time
from os import listdir
from tabulate import tabulate

from pyecol.heuristic import vizing_heuristic
from pyecol.counting import counting_colour
from pyecol.misra_gries import misra_gries
from pyecol.utils import ColouringGraph, validate_colouring, colours_used, \
    max_degree, dmacs2graph


benches = [
    "myciel3.col",
    "myciel4.col",
    "myciel5.col",
    "myciel6.col",
    "myciel7.col",
    "le450_5a.col",
    "le450_5b.col",
    "le450_5c.col",
    "le450_5d.col",
    "le450_15a.col",
    "le450_15b.col",
    "le450_15c.col",
    "le450_15d.col",
    "le450_25a.col",
    "le450_25b.col",
    "le450_25c.col",
    "le450_25d.col",
]


def benchmark():
    data = []
    for item in listdir("cols"):
        if item.endswith(".col") and item in benches:
            print(item)
            name = item[:-4]
            G = dmacs2graph(open(f"cols/{item}"))

            total_vh = 0
            total_cb = 0

            for _ in range(50):
                g = ColouringGraph.copy(G)
                start = time.monotonic()
                vizing_heuristic(g)
                end = time.monotonic()
                total_vh += end - start

            for _ in range(1):
                h = ColouringGraph.copy(G)
                misra_gries(h)

            for _ in range(50):
                h2 = ColouringGraph.copy(G)
                start = time.monotonic()
                counting_colour(h2)
                end = time.monotonic()
                total_cb += end - start

            data.append((
                name,
                max_degree(G),
                colours_used(g),
                colours_used(h),
                colours_used(h2),
                total_cb / total_vh,
            ))
            print(data[-1])
    data.sort()
    print(tabulate(data, headers=["Instance", "Δ", "ΔVh", "MG", "CB", "CB slowdown"]))


if __name__ == '__main__':
    benchmark()
