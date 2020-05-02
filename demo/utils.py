from subprocess import Popen, PIPE
import graphviz
from uuid import uuid4
from pyecol.utils import colours_used, max_degree, dmacs2graph, ColouringGraph
from pyecol.graph import Graph
from pyecol.misra_gries import misra_gries
from pyecol.heuristic import vizing_heuristic
from pyecol.counting import counting_colour


def lxc(graph, attempts=1):
    input_graph = graph2pt(graph)
    proc = Popen(
        ["../lxc/lxc", "-p", "-e", f"-a{attempts}"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    stdout, stderr = proc.communicate(input_graph)
    return lxc_edge_output_to_graph(stdout)


def gen_bipartite_graph(n, m):
    g = Graph(n + m)
    for u in range(n):
        for v in range(n, n + m):
            g[u, v] = 0
    return g


def graph2pt(g):
    V = sorted(g.nodes())
    m = []
    for u in V:
        x = []
        for v in V:
            x.append("0" if g.edge_data[u][v] is False else "1")
        m.append("".join(x))
    return "\n".join(m)


colours = ["#88CCEE", "#CC6677", "#DDCC77", "#117733",
           "#332288", "#AA4499", "#44AA99", "#999933",
           "#882255", "#661100", "#6699CC", "#888888"]
# colours = [
#     "#E41A1C",
#     "#377EB8",
#     "#4DAF4A",
#     "#984EA3",
#     "#FF7F00",
#     "#FFFF33",
#     "#A65628",
#     "#F781BF",
#     "#999999",
# ]


def render(g: Graph, name=None):
    ctx = graphviz.Graph(node_attr={"shape": "circle"})
    for u in g.nodes():
        ctx.node(str(u), str(u))

    offset = min(g[u, v] for u, v in g.edges())
    delta = max_degree(g)
    num_colours = colours_used(g)

    for u, v in g.edges():
        extra = {"label": str(g[u, v])}
        if num_colours <= len(colours):
            extra = {"color": colours[g[u, v] - offset]}
        ctx.edge(str(u), str(v), **extra)
    label = (
        (f'{name}\n' if name else '')
        + f'Class {1 if num_colours == delta else 2}\n'
        f'Δ = {delta}'
    )
    ctx.attr(label=label)
    ctx.render(
        f"tmp/{uuid4().hex}",
        view=True,
        quiet=True,
        quiet_view=True,
        cleanup=True,
    )


def lxc_edge_output_to_graph(output: str):
    lines = (x.strip() for x in output.splitlines())
    lines = [x for x in lines if x]
    n = len(lines)

    g = Graph(n)

    for i in range(n):
        adj = lines[i].split(",")[:-1]
        for j in range(n):
            if int(adj[j]) != -1:
                g.edge_data[i][j] = int(adj[j])
    return g
