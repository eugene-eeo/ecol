from bipartite import random_bipartite_graph, edge_colour_bipartite, \
        validate_colouring, plot_graph


def test_bipartite():
    for _ in range(1000):
        g = random_bipartite_graph()
        edge_colour_bipartite(g)
        if not validate_colouring(g):
            dot = plot_graph(g)
            dot.render('fail.gv', view=True)
            assert False


if __name__ == '__main__':
    test_bipartite()
