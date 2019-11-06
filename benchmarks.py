from os import listdir
from tabulate import tabulate

from heuristic import vizing_heuristic
from counting import counting_colour
from misra_gries import misra_gries
from utils import ColouringGraph, validate_colouring, colours_used, \
        max_degree, dmacs2graph


def benchmark():
    data = []
    for item in listdir("cols"):
        if item.endswith(".col"):
            name = item[:-4]
            G = dmacs2graph(open(f"cols/{item}"))
            g = ColouringGraph.copy(G)

            vizing_heuristic(g)
            assert validate_colouring(g)

            h = ColouringGraph.copy(G)

            misra_gries(h)
            assert validate_colouring(h)

            h2 = ColouringGraph.copy(G)

            counting_colour(h2)
            assert validate_colouring(h2)

            data.append((
                name,
                max_degree(G),
                colours_used(g),
                colours_used(h),
                colours_used(h2),
                ))
    data.sort()
    print(tabulate(data, headers=["Instance", "Δ", "ΔVh", "MG", "CB"]))


if __name__ == '__main__':
    benchmark()
