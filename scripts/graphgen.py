import sys
import random
import json
from graph import Graph
from utils import max_degree


# def erdos_renyi_graph(n, p, m):
#     r = random.Random()
#     g = Graph(n)
#     for i in range(n):
#         m_i = g.degree(i)
#         if m_i >= m:
#             continue
#         for j in range(i+1, n):
#             if r.random() <= p:
#                 g[i, j] = 0
#                 m_i += 1
#                 if m_i == m:
#                     break
#     return g


def deg_graph(n, m):
    g = Graph(n)
    d = {i: 0 for i in range(n)}
    for i in range(n):
        r = g.edge_data[i]
        s = [j for j in range(i+1, n) if d[j] < m and r[j] is False]
        mm = min(m - d[i], len(s))
        if mm > 0:
            k = random.randint(1, mm)
            u = random.sample(s, k)
            for j in u:
                g[i, j] = 0
                d[i] += 1
                d[j] += 1
    return g, d


def is_connected(G: Graph, core):
    for u in G.nodes():
        if u not in core:
            if not any(G.edge_data[u][z] is not False for z in core):
                return False
    return True


def is_cyclic(G, subset):
    visited = {x: False for x in subset}

    def cyclic_helper(v, visited, parent):
        visited[v] = True
        for i, x in enumerate(G.edge_data[v]):
            if x is not False and i in subset:
                if visited[i] is False:
                    if cyclic_helper(i, visited, v):
                        return True
                elif parent != i:
                    return True
        return False

    for node in subset:
        if not visited[node]:
            if cyclic_helper(node, visited, -1):
                return True
    return False


def is_overfull(G: Graph):
    return G.num_edges() > max_degree(G) * (G.n // 2)


def gen_sparse_graph(k, n, m=5):
    attempts = 100000
    while attempts > 0:
        attempts -= 1
        g, deg = deg_graph(n+k, m)
        d = max_degree(g)
        core = {x for x in range(n + k) if deg[x] == d}
        if len(core) > k:
            continue

        N = len(core)
        cand = set(g.nodes()) - core

        while N != k:
            if N > k:
                break

            i, j = random.sample(cand, 2)
            if g.edge_data[i][j] is False:
                g[i, j] = 0
                deg[i] += 1
                deg[j] += 1
                if deg[i] == d:
                    core.add(i)
                    cand.remove(i)
                    N += 1
                if deg[j] == d:
                    core.add(j)
                    cand.remove(j)
                    N += 1

        if len(core) != k \
                or not is_cyclic(g, core) \
                or is_overfull(g) \
                or not is_connected(g, core):
            continue
        return g


if __name__ == '__main__':
    for k in range(3, 6):
        for n in range(2, 5):
            for _ in range(100):
                g = gen_sparse_graph(k, n*k)
                if g is None:
                    break
                ed = g.edge_data
                edge_data = [[-1 if x is False else x for x in row] for row in ed]
                data = {
                    "k": k,
                    "n": n*k,
                    "edge_data": edge_data,
                }
                json.dump(data, sys.stdout)
                sys.stdout.write("\n")
                sys.stdout.flush()
