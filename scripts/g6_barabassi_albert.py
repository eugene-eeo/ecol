import sys
import math
import networkx as nx
import subprocess
import random


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


def _random_subset(seq, m):
    targets = set()
    while len(targets) < m:
        x = random.choice(seq)
        targets.add(x)
    return targets


def barabasi_albert_graph(n, m, seed=None):
    # Add m initial nodes (m0 in barabasi-speak)
    G = nx.complete_graph(m)
    # Target nodes for new edges
    targets = list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = []
    # Start adding the other n-m nodes. The first node is m.
    source = m
    while source < n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source]*m, targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source]*m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = _random_subset(repeated_nodes, m)
        source += 1
    return G


def main(end, attempts, repeats):
    #N = list(range(62, end, 2))
    N = [end]
    for n in N:
        for m in range((n*3)//4, n-1, 2):
            lines = []
            # count = 0
            for _ in range(repeats):
                g = barabasi_albert_graph(n, m)
                lines.append(graph_to_g6(g).encode('ascii'))
                # delta = max(d for _, d in g.degree())
                # if g.number_of_edges() > delta * (n // 2):
                #     count += 1

            proc = subprocess.Popen(
                ["lxc/lxc", "-a", str(attempts)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            stdout, _ = proc.communicate(b"\n".join(lines))
            class2 = len(stdout.strip().splitlines())
            print("%d,%d,%f" % (n, m, class2 / repeats))
            # print("%d,%d,%f" % (n, m, count / repeats))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: %s <n> <attempts> <repeats>" % sys.argv[0])
        exit(0)
    n = int(sys.argv[1])
    a = int(sys.argv[2])
    r = int(sys.argv[3])
    main(n, a, r)

    # n=50:
    # 50,40,0.000000
    # 50,41,0.000000
    # 50,42,0.000000
    # 50,43,0.000000
    # 50,44,0.012000
    # 50,45,0.456000
    # 50,46,0.760000
    # 50,47,0.928000
    # 50,48,0.940000

    # n=60:
    # 60,50,0.000000
    # 60,51,0.000000
    # 60,52,0.000000
    # 60,53,0.096000
    # 60,54,0.684000
    # 60,55,0.956000
    # 60,56,0.984000
    # 60,57,0.996000
    # 60,58,0.996000
