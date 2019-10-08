import random
import string
import networkx as nx
import graphviz


def random_bipartite_graph():
    A = random.sample(string.ascii_lowercase, random.randint(5, 10))
    B = random.sample(string.ascii_uppercase, random.randint(5, 10))
    G = nx.Graph()
    G.add_nodes_from(A)
    G.add_nodes_from(B)
    for u in A:
        neighbours = random.sample(B, random.randint(1, len(B)))
        G.add_edges_from([(u, v) for v in neighbours])
    return G


def plot_graph(G: nx.Graph):
    dot = graphviz.Graph()
    for node in G.nodes():
        dot.node(node, node)
    for u, v in G.edges():
        dot.edge(u, v, label=str(G.edges[u, v].get('colour', '0')))
    return dot


def max_degree(G: nx.Graph):
    return max(n for _, n in G.degree())


def free_colours(edges, colours):
    used = set(x['colour'] for _, x in edges.items() if 'colour' in x)
    return colours - used


def find_edge_with_colour(G, u, colour):
    for v in G[u]:
        if G.edges[u, v]['colour'] == colour:
            return u, v


def flip(G, start, alpha, beta):
    """
    Flips the edge colours along the path P starting on `start`
    in the graph G[`alpha`, `beta`]. E.g.:

            α      β      α      β
        v1 --> v2 --> v3 --> v4 --> v5

                flip(v1, α, β)

            β      α      β      α
        v1 --> v2 --> v3 --> v4 --> v5

    """
    u = start
    colour = alpha
    while True:
        edge = find_edge_with_colour(G, u, colour)
        if edge is None:
            break
        G.edges[edge]['colour'] = beta if colour == alpha else alpha
        u, _ = edge
        if u == start:
            break
        colour = beta if colour == alpha else alpha


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
