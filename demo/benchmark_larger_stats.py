import time
from utils import dmacs2graph, max_degree, lxc, colours_used

g = dmacs2graph(open('../cols/ash958GPIA.col'))

print("ash958GPIA")
print("|V|:", g.n)
print("|E|:", g.num_edges())
print("Δ:  ", max_degree(g))

start = time.time()
res = lxc(g)
end = time.time()

print(f"lxc: {colours_used(res)} ({end - start}s)")


# ==========================


g = dmacs2graph(open('../cols/wap04a.col'))

print("wap04a")
print("|V|:", g.n)
print("|E|:", g.num_edges())
print("Δ:  ", max_degree(g))
start = time.time()
res = lxc(g)
end = time.time()

print(f"lxc: {colours_used(res)} ({end - start}s)")
