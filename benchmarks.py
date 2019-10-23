from os import listdir
from tabulate import tabulate

from misra_gries import colours_used
from utils import ColouringGraph
from dmacs2graph import dmacs2graph
from heuristic import vizing_heuristic


def benchmark():
    data = []
    for item in listdir("cols"):
        if item.endswith(".col"):
            name = item[:-4]
            g = ColouringGraph.wrap(dmacs2graph(open(f"cols/{item}")))
            vizing_heuristic(g)
            data.append((name, colours_used(g)))
    data.sort()
    print(tabulate(data, headers=["Instance", "Colours Used"]))


if __name__ == '__main__':
    benchmark()
