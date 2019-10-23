from graph import Graph


def dmacs2graph(stream):
    g = None
    for line in stream:
        line = line.strip()
        if line.startswith('p'):
            _, format, nodes, _ = line.split()
            assert format.lower() == 'edge'
            n = int(nodes)
            g = Graph(n)
        elif line.startswith('e'):
            _, u, v = line.split()
            g[int(u)-1, int(v)-1] = 0
    return g
