import os
import glob
from pyecol.utils import dmacs2graph, max_degree


def main():
    data = []
    for f in glob.glob('../cols/*.col'):
        instance = f[len('../cols/'):]
        g = dmacs2graph(open(f))
        fname = 'pts/' + instance.replace('.col', '.pt')
        if not os.path.exists(fname):
            pt = "\n".join("".join("0" if e is False else "1" for e in row) for row in g.edge_data)
            pt += "\n"
            open(fname, 'w').write(pt)
        data.append([
            instance.replace('.col', ''),
            g.n,
            g.num_edges(),
            max_degree(g),
        ])

    data.sort()
    data = [("name", "n", "edges", "Δ")] + data
    for item in data:
        print(",".join(str(x) for x in item))


if __name__ == '__main__':
    main()
