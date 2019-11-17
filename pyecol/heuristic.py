from .utils import ColouringGraph, switch, get_path, max_degree


def vizing_heuristic(G: ColouringGraph):
    # http://www.din.uem.br/sbpo/sbpo2012/pdf/arq0521.pdf
    delta = max_degree(G)
    G.add_colours(set(range(1, delta + 1)))
    taboo = None

    while G.uncoloured_edges:
        if taboo is None:
            e_0 = w, v_0 = next(iter(G.uncoloured_edges))

        common = G.free[v_0] & G.free[w]
        if common:
            G[e_0] = common.pop()
            taboo = None
        else:
            available = G.free[v_0] - {taboo}
            if not available:
                G.add_colours({delta + 1})
                G[e_0] = delta+1
                taboo = None
            else:
                a_0 = available.pop()
                if taboo is None:
                    beta = next(iter(G.free[w]))
                P = get_path(G, v_0, beta, a_0)
                if P[-1] != w:
                    switch(G, P, beta, a_0)
                    G[e_0] = beta
                    taboo = None
                else:
                    e_1 = P[-2], P[-1]
                    G[e_1] = 0
                    G[e_0] = a_0
                    e_0 = e_1
                    v_0 = e_1[0]  # We know that w == P[-1]
                    taboo = a_0
    return G
