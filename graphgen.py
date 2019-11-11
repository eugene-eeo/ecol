import sys
import random
import json
from graph import erdos_renyi_graph, Graph
from utils import max_degree


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


def gen_sparse_graph(k, n, p=0.5):
    while True:
        g = erdos_renyi_graph(n+k, p)
        d = max_degree(g)
        core = {x for x in range(n + k) if g.degree(x) == d}
        if len(core) > k:
            continue

        N = len(core)
        cand = set(g.nodes()) - core

        while N != k:
            if N > k:
                break

            i, j = random.sample(cand, 2)
            g[i, j] = 0
            if g.degree(i) == d:
                core.add(i)
                cand.remove(i)
                N += 1
            if g.degree(j) == d:
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
    for k in range(3, 10):
        for n in [2, 4, 8, 16]:
            for _ in range(100):
                ed = gen_sparse_graph(k, n*k).edge_data
                edge_data = [[-1 if x is False else x for x in row] for row in ed]
                data = {
                    "k": k,
                    "n": n*k,
                    "edge_data": edge_data,
                }
                json.dump(data, sys.stdout)
                sys.stdout.write("\n")
