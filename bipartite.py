import random
import string
import networkx as nx
import graphviz
from itertools import cycle


def random_bipartite_graph():
    A = random.sample(string.ascii_lowercase, random.randint(2, 10))
    B = random.sample(string.ascii_uppercase, random.randint(2, 10))
    G = nx.Graph()
    G.add_nodes_from(A)
    G.add_nodes_from(B)
    for u in A:
        neighbours = random.sample(B, random.randint(1, len(B)))
        G.add_edges_from([(u, v) for v in neighbours])
    return G


def plot_graph(G: nx.Graph):
    dot = graphviz.Graph()
    dot.graph_attr['rankdir'] = 'LR'
    dot.graph_attr['ratio'] = '0.95'
    for node in G.nodes():
        dot.node(node, node)
    for u, v in G.edges():
        dot.edge(u, v, label=str(G.edges[u, v].get('colour', '0')))
    return dot


def max_degree(G: nx.Graph):
    return max(n for _, n in G.degree())


def free_colours(edges, colours):
    """
    Usage: free_colours(G[u], colours)
    """
    used = set(x['colour'] for _, x in edges.items() if 'colour' in x)
    return colours - used


def find_edge_with_colour(G, u, colour, exclude=()):
    for v in G[u]:
        if v not in exclude and G.edges[u, v].get('colour') == colour:
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
    u = start
    s = {u}
    for to_find, to_replace in cycle([(alpha, beta), (beta, alpha)]):
        edge = find_edge_with_colour(G, u, to_find, s)
        if edge is None:
            break
        G.edges[edge]['colour'] = to_replace
        _, u = edge
        if u == start:
            break
        s.add(u)


def edge_colour_bipartite(G: nx.Graph):
    colours = set(range(1, max_degree(G) + 1))
    for u, v in G.edges:
        u_free = free_colours(G[u], colours)
        v_free = free_colours(G[v], colours)
        common = u_free & v_free

        if common:
            colour = common.pop()
            G.edges[u, v]['colour'] = colour
            continue

        alpha = u_free.pop()
        beta = v_free.pop()
        flip(G, u, beta, alpha)
        G.edges[u, v]['colour'] = beta


def validate_colouring(G: nx.Graph):
    for u in G.nodes:
        x = {data['colour'] for data in G[u].values()}
        if len(x) != G.degree[u]:
            return False
    return True
