import networkx as nx
from bipartite import free_colours, max_degree, flip_path_containing


def rotate(G, v, W, colour):
    for i in range(len(W) - 1):
        G.edges[v, W[i]]['colour'] = G.edges[v, W[i+1]]['colour']
    G.edges[v, W[-1]]['colour'] = colour


def maximal_fan(G, X, Y, colours):
    F = [Y]
    S = set(G[X]) - {Y}
    found = True
    while found:
        found = False
        free = free_colours(G[F[-1]], colours)
        for v in S:
            if G.edges[X, v]['colour'] in free:
                F.append(v)
                S.remove(v)
                found = True
                break
    return F


def misra_gries(G: nx.Graph):
    # see http://www.cs.utexas.edu/users/misra/psp.dir/vizing.pdf
    colours = set(range(1, max_degree(G) + 2))  # Delta+1 colours
    for X, Y in G.edges:
        X_free = free_colours(G[X], colours)
        Y_free = free_colours(G[Y], colours)
        common = X_free & Y_free
        # easy case
        if common:
            G.edges[X, Y]['colour'] = common.pop()
            continue

        # construct a maximal fan:
        F = maximal_fan(G, X, Y, colours)

        c = X_free.pop()
        d = free_colours(G[F[-1]], colours).pop()
        flip_path_containing(G, X, c, d)

        for i, w in enumerate(F):
            if d in free_colours(G[w], colours):
                rotate(G, X, F[:i+1], d)
                break
    return G


def colours_used(G: nx.Graph):
    return len({edge_data['colour'] for edge_data in G.edges.values()})


def is_class_one(G: nx.Graph):
    return colours_used(G) == max_degree(G)
