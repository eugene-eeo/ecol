import sys
import math
import networkx as nx


# Bytes needed to write graph of size n
def bytes_needed(n):
    N = 1
    if n <= 62:
        N = 1
    elif N <= 258047:
        N = 4
    else:
        N = 8
    edges = (n * (n - 1)) / 2
    R = math.ceil(edges / 6)
    return N + R


def graph_to_g6(g: nx.Graph):
    n = g.number_of_nodes()
    N = 1
    buf = [0 for _ in range(bytes_needed(n))]
    if n <= 62:
        N = 1
        buf[0] = n
    elif N <= 258047:
        N = 4
        buf[0] = 126 - 63
        buf[1] = (n >> 12) & 63
        buf[2] = (n >> 6) & 63
        buf[3] = n & 63
    else:
        N = 8
        buf[0] = 126 - 63
        buf[1] = 126 - 63
        buf[2] = (n >> 30) & 63
        buf[3] = (n >> 24) & 63
        buf[4] = (n >> 18) & 63
        buf[5] = (n >> 12) & 63
        buf[6] = (n >> 6) & 63
        buf[7] = n & 63

    k = 0
    for v in range(n):
        for u in range(v):
            i = k // 6
            j = 5 - (k % 6)
            if g.edges.get((u, v)) is not None:
                buf[N + i] |= 1 << j
            k += 1

    for i, b in enumerate(buf):
        buf[i] = b + 63
    return "".join(map(chr, buf))


def gen_graph(n, delta):
    for m in range(3, n-1):
        deg_sequence = [delta - 1] * (n - m) + [delta] * m
        for _ in range(100):
            try:
                g = nx.random_degree_sequence_graph(deg_sequence, tries=100)
                d = g.degree()
                core = g.subgraph([u for u in range(n) if d[u] == delta])
                if max(dict(core.degree()).values()) == 2:
                    yield g
            except nx.exception.NetworkXUnfeasible:
                pass
            except nx.exception.NetworkXError:
                break


if __name__ == '__main__':
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        delta = int(sys.argv[3])
    except IndexError:
        print(f"usage: {sys.argv[0]} <start> <end> <delta>")
        exit(1)

    for n in range(start, end):
        print(f"n={n}", file=sys.stderr)
        for g in gen_graph(n, delta):
            print(graph_to_g6(g))
