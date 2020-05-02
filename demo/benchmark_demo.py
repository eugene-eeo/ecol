from utils import *

g = dmacs2graph(open('../cols/myciel3.col'))

g1 = ColouringGraph.copy(g)
g2 = ColouringGraph.copy(g)
g3 = ColouringGraph.copy(g)

vizing_heuristic(g1)
misra_gries(g2)
counting_colour(g3)

render(g1, name="myciel3 (vizing heuristic)")
render(g2, name="myciel3 (misra gries)")
render(g3, name="myciel3 (counting-based)")
