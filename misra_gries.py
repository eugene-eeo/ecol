import networkx as nx
from bipartite import free_colours, max_degree, flip_path_containing


def rotate(G, v, W, colour):
    for i in range(len(W) - 1):
        G.edges[v, W[i]]['colour'] = G.edges[v, W[i+1]]['colour']
    G.edges[v, W[-1]]['colour'] = colour


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
        F = [Y]
        S = set(F)
        found = True
        while found:
            found = False
            for v in G[X]:
                if (v not in S and
                        G.edges[X, v]['colour'] in
                        free_colours(G[F[-1]], colours)):
                    F.append(v)
                    S.add(v)
                    found = True
                    break

        c = X_free.pop()
        d = free_colours(G[F[-1]], colours).pop()
        flip_path_containing(G, X, c, d)

        for w in F:
            if d in free_colours(G[w], colours):
                rotate(G, X, F[:F.index(w)+1], d)
                break
