from functools import reduce
from utils import ColouringGraph, max_degree, switch, get_path_subset


def counting_colour(G: ColouringGraph):
    # https://arxiv.org/pdf/1901.01861.pdf
    delta = max_degree(G)
    # Allocate 1...delta+1 colours
    G.add_colours(set(range(1, delta + 2)))

    V = set()
    uncoloured = set(G.nodes())

    while uncoloured:
        u = uncoloured.pop()
        W = set()
        for v in V:
            d = G.edge_data[u][v]
            if d is not False and d == 0:
                W.add(v)

        # Avoid allocation of V | {u} when calculating the path;
        # it hurts the niceness of our program in the name of efficiency
        V.add(u)
        F_u = {v: G.free[u] & G.free[v] for v in W}

        while W:
            common = reduce(set.union, F_u.values())
            found = False
            for l_c in common:
                # Case (1)
                Z = [z for z in W if l_c in F_u[z]]  # All uz that miss l_c
                found = sum(1 for z in Z if len(F_u[z]) <= 2) <= 1
                if found:
                    v = min(Z, key=lambda z: len(F_u[z]))
                    G[u, v] = l_c
                    W.remove(v)
                    del F_u[v]
                    # Need to recalculate
                    for fset in F_u.values():
                        fset.discard(l_c)
                    break

            if found:
                continue

            # Case (2)
            # There must exist a b
            b = min(G.free[u] - common)
            # Pick a w
            w = min(W, key=lambda v: len(F_u[v]))
            # consider a colour 'a'
            a = min(F_u[w])
            P = get_path_subset(G, w, V, b, a)
            switch(G, P, b, a)
            G[u, w] = b
            if P[-1] in W:
                F_u[P[-1]].remove(a)
            W.remove(w)
            del F_u[w]
    return G
