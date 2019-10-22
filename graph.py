import random


# optimised undirected graph class
class Graph:
    __slots__ = ('n', 'edge_data')

    def __init__(self, n):
        self.n = n
        self.edge_data = [[False] * n for _ in range(n)]

    def __getitem__(self, edge):
        x, y = edge
        return self.edge_data[x][y]

    def __setitem__(self, edge, data):
        x, y = edge
        self.edge_data[x][y] = data
        self.edge_data[y][x] = data

    def nodes(self):
        return range(self.n)

    def degree(self, node):
        return sum(1 for x in self.edge_data[node] if x is not False)

    def edges(self):
        for i in range(self.n):
            row = self.edge_data[i]
            for j in range(i+1, self.n):
                if row[j] is not False:
                    yield (i, j)

    def neighbours(self, node):
        for i, data in enumerate(self.edge_data[node]):
            if data is not False:
                yield i


def complete_graph(k):
    g = Graph(k)
    for i in range(k):
        for j in range(i+1, k):
            g[i, j] = 0
    return g


def erdos_renyi_graph(n, p):
    r = random.Random()
    g = Graph(n)
    for i in range(n):
        for j in range(n):
            if r.random() <= p:
                g[i, j] = 0
    return g
