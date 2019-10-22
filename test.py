from graph import complete_graph, erdos_renyi_graph
from misra_gries import misra_gries
from bipartite import random_bipartite_graph, edge_colour_bipartite, \
        validate_colouring


def test_bipartite():
    print("Testing for bipartite graphs")
    for _ in range(1000):
        g = random_bipartite_graph()
        edge_colour_bipartite(g)
        assert validate_colouring(g)


def test_general():
    print("Testing for K_n")
    for n in range(10, 60):
        g = complete_graph(n)
        misra_gries(g)
        assert validate_colouring(g)


def test_random():
    print("Testing for G(n,p)")
    for n in range(10, 60):
        for p in [0.1, 0.2, 0.4, 0.8, 0.9]:
            g = erdos_renyi_graph(n, p)
            misra_gries(g)
            assert validate_colouring(g)


if __name__ == '__main__':
    test_bipartite()
    test_general()
    test_random()
