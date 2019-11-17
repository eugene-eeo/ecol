from .utils import max_degree, switch_path_containing, ColouringGraph


def rotate(G: ColouringGraph, v, W, colour):
    colours = []
    for x in W:
        colours.append(G[v, x])
        G[v, x] = 0

    for i in range(len(W) - 1):
        G[v, W[i]] = colours[i+1]
    G[v, W[-1]] = colour


def maximal_fan(G: ColouringGraph, X, Y):
    F = [Y]
    S = set(G.neighbours(X)) - {Y}
    found = True
    while found and S:
        found = False
        free = G.free[F[-1]]
        for v in S:
            if G[X, v] in free:
                F.append(v)
                S.remove(v)
                found = True
                break
    return F


def misra_gries(G: ColouringGraph) -> ColouringGraph:
    # see http://www.cs.utexas.edu/users/misra/psp.dir/vizing.pdf
    G.add_colours(set(range(1, max_degree(G) + 2)))  # Delta+1 colours
    for X, Y in G.edges():
        X_free = G.free[X]
        Y_free = G.free[Y]
        common = X_free & Y_free
        # easy case
        if common:
            G[X, Y] = min(common)
            continue

        # construct a maximal fan:
        F = maximal_fan(G, X, Y)

        c = min(X_free)
        d = min(G.free[F[-1]])
        switch_path_containing(G, X, c, d)

        for i, w in enumerate(F):
            if d in G.free[w]:
                rotate(G, X, F[:i+1], d)
                break
    return G
