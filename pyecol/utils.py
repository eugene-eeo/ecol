import graphviz
from itertools import cycle
from .graph import Graph


class ColouringGraph(Graph):
    def __init__(self, n, edge_data):
        self.n = n
        self.edge_data = edge_data
        self.uncoloured_edges = set(self.edges())
        self.free = [set() for v in self.nodes()]

    @classmethod
    def wrap(cls, g: Graph):
        return ColouringGraph(g.n, g.edge_data)

    @classmethod
    def copy(cls, g: Graph):
        return ColouringGraph(g.n, [x[:] for x in g.edge_data])

    def add_colours(self, colours):
        for fc in self.free:
            fc.update(colours)

    def __setitem__(self, edge, colour):
        og = self[edge]
        x, y = edge
        if x > y:
            x, y = y, x
        if og != 0:
            self.free[x].add(og)
            self.free[y].add(og)

        # an uncolour operation
        if colour == 0:
            self.uncoloured_edges.add((x, y))
        else:
            self.free[x].discard(colour)
            self.free[y].discard(colour)
            self.uncoloured_edges.discard((x, y))

        super().__setitem__(edge, colour)


def switch(G: ColouringGraph, P: [int], alpha, beta):
    for i in range(len(P)-1):
        G[P[i], P[i+1]] = 0

    swatch = [beta, alpha]
    for i in range(len(P)-1):
        G[P[i], P[i+1]] = swatch[i % 2]


def find_edge_with_colour_subset(G: ColouringGraph, u, colour, subset: set):
    for v in subset.intersection(G.neighbours(u)):
        if G[u, v] == colour:
            return u, v


def get_path_subset(G: ColouringGraph, v, subset, alpha, beta) -> [int]:
    path = [v]
    for colour in cycle([alpha, beta]):
        edge = find_edge_with_colour_subset(G, path[-1], colour, subset)
        if edge is None:
            break
        _, next = edge
        path.append(next)
    return path


def find_edge_with_colour(G: ColouringGraph, u, colour, prev=None):
    for v in G.neighbours(u):
        if G[u, v] == colour and v != prev:
            return u, v


def get_path(G: ColouringGraph, v, alpha, beta) -> [int]:
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


def switch_path_containing(G: ColouringGraph, v, alpha, beta) -> [int]:
    P = get_path(G, v, alpha, beta)
    Q = get_path(G, v, beta, alpha)
    Q.reverse()
    Q.pop()
    colours = (alpha, beta) if len(Q) % 2 == 0 else (beta, alpha)
    Q.extend(P)
    switch(G, Q, *colours)


def max_degree(G: Graph):
    return max(G.degree(n) for n in G.nodes())


def plot_graph(G: Graph, with_labels=True, node_label="node_num", core_same_rank=True, nice_core=False):
    dot = graphviz.Graph()
    # dot.graph_attr['rankdir'] = 'LR'
    # dot.graph_attr['ratio'] = '0.95'

    delta = max_degree(G)
    nodes = set(G.nodes())
    degrees = {x: G.degree(x) for x in G.nodes()}
    core = {x for x in degrees if degrees[x] == delta}

    def get_label(node):
        if node_label == "node_num":
            return str(node)
        return str(degrees[node])

    if nice_core:
        core_nodes = set(core)
        adj = {x: set(G.neighbours(x)) & set(core_nodes) for x in core}
        values = set(len(adj[x]) for x in adj)
        for deg in sorted(values):
            with dot.subgraph() as s:
                s.attr(rank='same')
                s.attr('node', style='solid,filled', color='black', fillcolor='grey')
                for node in core:
                    if len(adj[node]) == deg:
                        s.node(str(node), get_label(node))

    else:
        with dot.subgraph() as s:
            if core_same_rank:
                s.attr(rank='same')
            s.attr('node', style='solid,filled', color='black', fillcolor='grey')
            for node in core:
                s.node(str(node), get_label(node))

    for node in nodes - core:
        dot.node(str(node), get_label(node))

    for u, v in G.edges():
        if with_labels:
            dot.edge(str(u), str(v), label=str(G[u, v]))
        else:
            dot.edge(str(u), str(v))

    colours = colours_used(G)
    graph_class = 1 if colours == delta else (2 if colours == delta+1 else '?')
    deg_seq = sorted(degrees.values())
    dot.attr(label=rf'Δ = {delta}\nClass {graph_class}\n{deg_seq}')
    return dot


def validate_colouring(G: Graph):
    for u in G.nodes():
        x = {G[u, v] for v in G.neighbours(u)}
        if len(x) != G.degree(u):
            return False
    return True


def colours_used(G: ColouringGraph):
    return len({G[edge] for edge in G.edges()})


def is_class_one(G: ColouringGraph):
    return colours_used(G) == max_degree(G)


def dmacs2graph(stream):
    g = None
    for line in stream:
        line = line.strip()
        if line.startswith('p'):
            _, _, nodes, _ = line.split()
            n = int(nodes)
            g = Graph(n)
            break
    for line in stream:
        if line.startswith('e'):
            _, u, v = line.split()
            g[int(u)-1, int(v)-1] = 0
    return g


def is_overfull(g: Graph) -> bool:
    return g.num_edges() > max_degree(g) * (g.n // 2)


def contains_cycle(g: Graph, subset=None):
    subset = subset if subset is not None else set(g.nodes())

    # A recursive function that uses visited[] and parent to detect
    # cycle in subgraph reachable from vertex v.
    def isCyclicUtil(v, visited, parent):

        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in subset & set(g.neighbours(v)):
            # If the node is not visited then recurse on it
            if not visited[i]:
                if isCyclicUtil(i, visited, v):
                    return True
            # If an adjacent vertex is visited and not parent of current vertex,
            # then there is a cycle
            elif parent != i:
                return True

        return False

    visited = {x: False for x in subset}
    for i in subset:
        if not visited[i]:
            if isCyclicUtil(i, visited, -1):
                return True
    return False


def golang_graph_to_graph(edge_data) -> Graph:
    """
    Convert golang graph to pyecol graph.
    Go implementation uses -1 for no-edge instead of False.
    """
    g = Graph(len(edge_data))
    g.edge_data = [[(False if x == -1 else 0) for x in row] for row in edge_data]
    return g


def graph_to_golang_graph(g: Graph) -> list:
    """
    Convert from pyecol graph to golang graph.
    Go implementation uses -1 for no-edge instead of False.
    """
    return [[(-1 if x is False else x) for x in row] for row in g.edge_data]
