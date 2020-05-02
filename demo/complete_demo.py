from utils import *
from pyecol.graph import complete_graph


g = complete_graph(20)

h1 = ColouringGraph.copy(g)
h2 = ColouringGraph.copy(g)
h3 = ColouringGraph.copy(g)

vizing_heuristic(h1)
counting_colour(h2)
misra_gries(h3)

print("VH:", colours_used(h1))
print("CB:", colours_used(h2))
print("MG:", colours_used(h3))


print("LXC:")
for i in range(1, 40, 4):
    colours = colours_used(lxc(g, attempts=i))
    print("  ", i, colours, "(Class 1)" if colours == max_degree(g) else "(Class 2)")
