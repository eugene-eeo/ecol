from os import listdir
from tabulate import tabulate

from utils import ColouringGraph, validate_colouring, colours_used
from dmacs2graph import dmacs2graph
from heuristic import vizing_heuristic
from misra_gries import misra_gries


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

            data.append((name, colours_used(g), colours_used(h)))
    data.sort()
    print(tabulate(data, headers=["Instance", "ΔVh", "MG"]))


if __name__ == '__main__':
    benchmark()
