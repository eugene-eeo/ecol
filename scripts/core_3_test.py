import networkx as nx
import json
import sys


def main():
    for n in range(3, 20):
        core = [2*n] * 3
        for i in range(n):
            for j in range(2, 2*n, 2):
                # i == how many nodes to reduce the degree
                # j == how much degree reduction
                # G ~= (2n-1)^(2n-2) (2n)^3 <=> G is class 2
                deg_sequence = core \
                    + [2*n-j] * (2*i) \
                    + [2*n-1] * (2*n-2 - 2*i)
                try:
                    g = nx.havel_hakimi_graph(deg_sequence)
                except nx.exception.NetworkXError:
                    continue
                m = g.number_of_nodes()
                edge_data = [[-1] * m for _ in range(m)]
                for u, v in g.edges():
                    edge_data[u][v] = 0
                    edge_data[v][u] = 0
                json.dump({
                    "d": i,
                    "j": j,
                    "n": n,
                    "expected_class_two": i == 0,
                    "edge_data": edge_data,
                }, sys.stdout)
                sys.stdout.write("\n")
                if i == 0:
                    break


if __name__ == '__main__':
    main()
