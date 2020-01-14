from itertools import combinations, product
from pyecol.graph import Graph
from pyecol.utils import max_degree


def attach_core(delta, core: Graph, out: Graph):
    # Cannot construct if we have less nodes than delta
    if out.n + core.n < delta:
        return

    core_nodes = list(core.nodes())
    out_nodes = list(out.nodes())

    attach = list(combinations(out_nodes, delta - max_degree(core)))
    for attachs in product(attach, repeat=len(core_nodes)):
        print(attachs)
        g = Graph(core.n + out.n)
        m = out.n

        for u, v in core.edges():
            g[u, v] = 0

        for u, v in out.edges():
            g[u + m, v + m] = 0

        bad = False

        d = g.degrees()
        for u, peers in enumerate(attachs):
            for v in peers:
                g[u, v + m] = 0
                d[u] += 1
                d[v + m] += 1
                if d[u] > delta or d[v + m] >= delta:
                    bad = True
                    break
            if bad:
                break

        if bad:
            continue
        yield g
