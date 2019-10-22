from graph import complete_graph, erdos_renyi_graph
from misra_gries import misra_gries
from heuristic import vizing_heuristic
from bipartite import random_bipartite_graph, validate_colouring


def test_bipartite(f):
    print("  Testing for bipartite graphs")
    for _ in range(1000):
        g = random_bipartite_graph()
        f(g)
        assert validate_colouring(g)


def test_general(f):
    print("  Testing for K_n")
    for n in range(10, 60):
        g = complete_graph(n)
        f(g)
        assert validate_colouring(g)


def test_random(f):
    print("  Testing for G(n,p)")
    for n in range(10, 60):
        for p in [0.1, 0.2, 0.4, 0.8, 0.9]:
            g = erdos_renyi_graph(n, p)
            f(g)
            assert validate_colouring(g)


if __name__ == '__main__':
    for f in [misra_gries, vizing_heuristic]:
        print(f"{f.__name__}:")
        test_bipartite(f)
        test_general(f)
        test_random(f)
