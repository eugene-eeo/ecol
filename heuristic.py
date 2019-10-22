from graph import Graph
from bipartite import max_degree, find_edge_with_colour
from itertools import cycle


def switch(G: Graph, P: [int], alpha, beta, unset_colour, set_colour):
    for i in range(len(P)-1):
        unset_colour((P[i], P[i+1]))

    swatch = [beta, alpha]
    for i in range(len(P)-1):
        set_colour((P[i], P[i+1]), swatch[i % 2])


def get_path(G: Graph, v, alpha, beta) -> [int]:
    prev = None
    path = [v]
    for colour in cycle([alpha, beta]):
        edge = find_edge_with_colour(G, path[-1], colour, prev)
        if edge is None:
            break
        prev = path[-1]
        _, next = edge
        path.append(next)
    return path


def vizing_heuristic(G: Graph):
    # http://www.din.uem.br/sbpo/sbpo2012/pdf/arq0521.pdf
    delta = max_degree(G)
    free = {v: set(range(1, delta + 1)) for v in G.nodes()}
    taboo = None
    uncoloured = set(G.edges())

    def set_colour(edge, colour):
        x, y = edge
        G[edge] = colour
        free[x].remove(colour)
        free[y].remove(colour)
        uncoloured.remove(edge)

    def unset_colour(edge):
        x, y = edge
        free[x].add(G[edge])
        free[y].add(G[edge])
        G[edge] = 0
        uncoloured.add(edge)

    while uncoloured:
        if taboo is None:
            e_0 = w, v_0 = next(iter(uncoloured))

        common = free[v_0] & free[w]
        if common:
            set_colour(e_0, common.pop())
            taboo = None
        else:
            available = free[v_0] - {taboo}
            if not available:
                for fc in free.values():
                    fc.add(delta + 1)
                set_colour(e_0, delta+1)
                taboo = None
            else:
                a_0 = available.pop()
                if taboo is None:
                    beta = next(iter(free[w]))
                P = get_path(G, v_0, beta, a_0)
                if P[-1] != w:
                    switch(G, P, beta, a_0, unset_colour, set_colour)
                    set_colour(e_0, beta)
                    taboo = None
                else:
                    e_1 = P[-2], P[-1]
                    unset_colour(e_1)
                    set_colour(e_0, a_0)
                    e_0 = e_1
                    v_0 = e_1[0]  # We know that w == P[-1]
                    taboo = a_0
    return G
