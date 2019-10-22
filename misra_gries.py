from graph import Graph
from bipartite import free_colours, max_degree, flip_path_containing


def rotate(G, v, W, colour):
    for i in range(len(W) - 1):
        G[v, W[i]] = G[v, W[i+1]]
    G[v, W[-1]] = colour


def maximal_fan(G: Graph, X, Y, colours):
    F = [Y]
    S = set(G.neighbours(X)) - {Y}
    found = True
    while found:
        found = False
        free = free_colours(G, F[-1], colours)
        for v in S:
            if G[X, v] in free:
                F.append(v)
                S.remove(v)
                found = True
                break
    return F


def misra_gries(G: Graph):
    # see http://www.cs.utexas.edu/users/misra/psp.dir/vizing.pdf
    colours = set(range(1, max_degree(G) + 2))  # Delta+1 colours
    for X, Y in G.edges():
        X_free = free_colours(G, X, colours)
        Y_free = free_colours(G, Y, colours)
        common = X_free & Y_free
        # easy case
        if common:
            G[X, Y] = min(common)
            continue

        # construct a maximal fan:
        F = maximal_fan(G, X, Y, colours)

        c = min(X_free)
        d = min(free_colours(G, F[-1], colours))
        flip_path_containing(G, X, c, d)

        for i, w in enumerate(F):
            if d in free_colours(G, w, colours):
                rotate(G, X, F[:i+1], d)
                break
    return G


def colours_used(G: Graph):
    return len({G[edge] for edge in G.edges()})


def is_class_one(G: Graph):
    return colours_used(G) == max_degree(G)
