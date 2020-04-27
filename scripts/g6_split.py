import sys
import random
import networkx as nx
import math
import subprocess


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


def gen_split_graph(m, n, p):
    g = nx.Graph()
    for i in range(m):
        for j in range(i+1, m):
            g.add_edge(i, j)

    for i in range(n):
        for j in range(m):
            if random.random() <= p:
                g.add_edge(j, m+i)

    return g


P = [x/100 for x in range(0, 101)]
#P = [0, 0.125, 0.25, 0.5, 0.75, 0.95, 1.0]


def main():
    for m in [8]:
        # for n in range(m + 2, m + 2 + 1):
        for n in [1, 2, 3, 4, 5, 6, 7]:
            # for p in [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.19, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99, 0.991, 0.992, 0.993, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999, 1.0]:
            for p in P:
                lines = []
                repeats = 500
                for _ in range(repeats):
                    lines.append(graph_to_g6(gen_split_graph(m, n, p)).encode('ascii'))
                proc = subprocess.Popen(
                    ["lxc/lxc", "-a", str(5000)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                stdout, _ = proc.communicate(b"\n".join(lines))
                class2 = len(stdout.strip().splitlines())
                print("%d,%d,%f,%f" % (m, n, p, class2 / repeats))
                sys.stdout.flush()


if __name__ == '__main__':
    main()
