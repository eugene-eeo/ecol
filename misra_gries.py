import networkx as nx
from bipartite import free_colours, max_degree, find_edge_with_colour, \
    flip_path_containing


def endpoint_with_colour(G, u, colour):
    _, v = find_edge_with_colour(G, u, colour)
    return v


def rotate(G, v, W, colour):
    for i in range(len(W) - 1):
        G.edges[v, W[i]]['colour'] = G.edges[v, W[i+1]]['colour']
    G.edges[v, W[-1]]['colour'] = colour


def misra_gries(G: nx.Graph):
    colours = set(range(1, max_degree(G) + 2))  # Delta+1 colours
    print(colours)
    for X, Y in G.edges:
        X_free = free_colours(G[X], colours)
        Y_free = free_colours(G[Y], colours)
        common = X_free & Y_free
        # easy case
        if common:
            G.edges[X, Y]['colour'] = common.pop()
            continue

        # construct a maximal fan:
        F = [Y]
        found = True
        while found:
            found = False
            for v in G[X]:
                if v not in F and \
                        G.edges[X, v].get('colour') is not None and \
                        G.edges[X, v]['colour'] in free_colours(G[F[-1]], colours):
                    F.append(v)
                    found = True
                    break

        c = X_free.pop()
        d = free_colours(G[F[-1]], colours).pop()
        flip_path_containing(G, X, c, d)

        w = None
        for x in F:
            if d in free_colours(G[x], colours):
                w = x
                break
        if w is not None:
            rotate(G, X, F[:F.index(w)+1], d)
