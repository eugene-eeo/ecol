import random
import string
import graphviz
from graph import Graph
from itertools import cycle


def random_bipartite_graph():
    A = random.sample(string.ascii_lowercase, random.randint(2, 23))
    B = random.sample(string.ascii_uppercase, random.randint(2, 23))
    G = Graph(len(A) + len(B))
    for i, u in enumerate(A):
        neighbours = random.sample(B, random.randint(1, len(B)))
        for x in neighbours:
            G[i, len(A) + B.index(x)] = 0
    return G


def plot_graph(G: Graph):
    dot = graphviz.Graph()
    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr['ratio'] = '0.95'
    for node in G.nodes():
        dot.node(str(node), str(node))
    for u, v in G.edges():
        dot.edge(str(u), str(v), label=str(G[u, v]))
    return dot


def max_degree(G: Graph):
    return max(G.degree(n) for n in G.nodes())


def free_colours(G: Graph, u, colours: set):
    """
    Usage: free_colours(G, u, colours)
    """
    return colours.difference(G[u, v] for v in G.neighbours(u))


def flip_path_containing(G, v, alpha, beta):
    """
    Flips the edge colours along the path P containing `v`
    in the graph G[`alpha`,`beta`]. E.g.:

             β     α      β      α
        u-1 --> v --> u1 --> u2 --> ...

    """
    #      α     β     α     β
    # ... --> y --> v --> x --> ...
    e = find_edge_with_colour(G, v, alpha)
    f = find_edge_with_colour(G, v, beta)
    if e:
        _, x = e
        flip(G, x, beta, alpha)
        G[e] = beta
    if f:
        _, y = f
        flip(G, y, alpha, beta)
        G[f] = alpha


def find_edge_with_colour(G: Graph, u, colour, prev=None):
    for v in G.neighbours(u):
        if G[u, v] == colour and v != prev:
            return u, v


def flip(G, start, alpha, beta):
    """
    Flips the edge colours along the path P starting on `start`
    in the graph G[`alpha`,`beta`]. E.g.:

            α      β      α      β
        v1 --> v2 --> v3 --> v4 --> v5

                flip(v1, α, β)

            β      α      β      α
        v1 --> v2 --> v3 --> v4 --> v5

    """
    prev = None
    u = start
    for to_find, to_replace in cycle([(alpha, beta), (beta, alpha)]):
        edge = find_edge_with_colour(G, u, to_find, prev)
        prev = u
        if edge is None:
            break

        G[edge] = to_replace
        _, u = edge
        if u == start:
            break


def edge_colour_bipartite(G: Graph):
    colours = set(range(1, max_degree(G) + 1))
    for u, v in G.edges():
        u_free = free_colours(G, u, colours)
        v_free = free_colours(G, v, colours)
        common = u_free & v_free

        if common:
            G[u, v] = common.pop()
            continue

        alpha = u_free.pop()
        beta = v_free.pop()
        flip(G, u, beta, alpha)
        G[u, v] = beta


def validate_colouring(G: Graph):
    for u in G.nodes():
        x = {G[u, v] for v in G.neighbours(u)}
        if len(x) != G.degree(u):
            return False
    return True
