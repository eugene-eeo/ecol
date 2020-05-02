from utils import *


g = gen_bipartite_graph(2, 5)
render(lxc(g), "Bipartite 2, 5")


print("Δ   colours used")
for i in range(10, 850, 50):
    g = gen_bipartite_graph(i, i)
    print("{:<3} {}".format(
        max_degree(g),
        colours_used(lxc(g)),
    ))
