# check_claim_odd.py
# ==================
#
# Check if we can wrap K_n where n is odd with G.
# To make it a bad core.

from pyecol.graph import Graph


def construct(m):
    assert m % 2 == 1 and m >= 7
    g = Graph(m + 5)

    # Complete graph on m
    for u in range(m):
        for v in range(u+1, m):
            g[u, v] = 0

    # initialize extension
    # deg( m   ) = 1
    # deg( m+1 ) = m
    # deg( m+2 ) = m
    # deg( m+3 ) = m+1
    # deg( m+4 ) = m+1
    g[m, m-1] = 0
    g[m+1, m+3] = 0
    g[m+1, m+4] = 0
    g[m+2, m+3] = 0
    g[m+2, m+4] = 0
    g[m+3, m+4] = 0

    for u in range(0, m-2):
        g[m+1, u] = 0

    return g
