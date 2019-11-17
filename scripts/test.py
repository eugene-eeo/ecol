from pyecol.graph import complete_graph, erdos_renyi_graph, complete_bipartite_graph
from pyecol.utils import validate_colouring, ColouringGraph
from pyecol.misra_gries import misra_gries
from pyecol.heuristic import vizing_heuristic
from pyecol.counting import counting_colour


def test_bipartite(f):
    print("  Testing for bipartite graphs")
    for n in range(2, 51):
        for m in range(n+1, 51):
            g = ColouringGraph.wrap(complete_bipartite_graph(n, m))
            f(g)
            assert validate_colouring(g)


def test_general(f):
    print("  Testing for K_n")
    for n in range(10, 61):
        g = ColouringGraph.wrap(complete_graph(n))
        f(g)
        assert validate_colouring(g)


def test_random(f):
    print("  Testing for G(n,p)")
    for n in range(10, 61):
        for p in [0.1, 0.2, 0.4, 0.8, 0.9]:
            g = ColouringGraph.wrap(erdos_renyi_graph(n, p))
            f(g)
            assert validate_colouring(g)


if __name__ == '__main__':
    for f in [misra_gries, vizing_heuristic, counting_colour]:
        print(f"{f.__name__}:")
        test_bipartite(f)
        test_general(f)
        test_random(f)
