import random
import string
import networkx as nx
import graphviz
from itertools import cycle


def random_bipartite_graph():
    A = random.sample(string.ascii_lowercase, random.randint(2, 23))
    B = random.sample(string.ascii_uppercase, random.randint(2, 23))
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
        dot.node(str(node), str(node))
    for u, v in G.edges():
        dot.edge(str(u), str(v), label=str(G.edges[u, v].get('colour', '0')))
    return dot


def max_degree(G: nx.Graph):
    return max(n for _, n in G.degree())


def used_colours(edges):
    """
    Usage: used_colours(G[u])
    """
    return set(x['colour'] for _, x in edges.items() if 'colour' in x)


def free_colours(edges, colours):
    """
    Usage: free_colours(G[u], colours)
    """
    return colours - used_colours(edges)


def coloured_component_endpoint(G, start, alpha, beta):
    u = start
    prev = u
    for to_find in cycle([alpha, beta]):
        edge = find_edge_with_colour(G, u, to_find, prev)
        if edge is None:
            return prev
        prev = u
        _, u = edge
        if u != start:
            break


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
        G.edges[e]['colour'] = beta
    if f:
        _, y = f
        flip(G, y, alpha, beta)
        G.edges[f]['colour'] = alpha


def find_edge_with_colour(G, u, colour, prev=None):
    for v in G[u]:
        if G.edges[u, v].get('colour') == colour and v != prev:
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

        G.edges[edge]['colour'] = to_replace
        _, u = edge
        if u == start:
            break


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
            print(u)
            return False
    return True
