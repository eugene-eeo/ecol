import json
from pyecol.utils import golang_graph_to_graph, plot_graph

u = []
for line in open('k9_core.jsonl'):
    g = golang_graph_to_graph(json.loads(line)['edge_data'])
    if sorted(g.degrees().values()) == [1, 9, 9, 10, 10] + [11]*9:
        u.append(g)

for i, g in enumerate(u):
    plot_graph(g, with_labels=False, node_label="degree").render(f'k9_core/k9_core.{g.n}.{i}', view=False, cleanup=True)


print(plot_graph(u[0], with_labels=False, node_label="degree").source)


u = []
for line in open('k7_core.jsonl'):
    g = golang_graph_to_graph(json.loads(line)['edge_data'])
    if sorted(g.degrees().values()) == [1, 7, 7, 8, 8] + [9]*7:
        u.append(g)

for i, g in enumerate(u):
    plot_graph(g, with_labels=False, node_label="degree").render(f'k7_core/k7_core.{g.n}.{i}', view=False, cleanup=True)


# print(plot_graph(u[4], with_labels=False, node_label="degree").source)
