## Benchmark instances

    Instance      Δ    ΔVh    MG    CB
    ----------  ---  -----  ----  ----
    le450_15a    99     99    99    99
    le450_15b    94     94    94    94
    le450_15c   139    139   140   139
    le450_15d   138    138   138   138
    le450_25a   128    128   128   128
    le450_25b   111    111   111   111
    le450_25c   179    179   179   179
    le450_25d   157    157   157   157
    le450_5a     42     42    42    42
    le450_5b     42     42    43    42
    le450_5c     66     66    67    66
    le450_5d     68     68    69    68
    myciel3       5      5     6     5
    myciel4      11     11    12    11
    myciel5      23     23    23    23
    myciel6      47     47    47    47
    myciel7      95     95    95    95

# Bad cores

 - `K_n` (even n, n >= 4) is always bad core.
 - `K_n` (odd n, n >= 5) is always bad core (but can't find common substructure),
 but degree sequence looks like:
   - `n=5`: 1, `(n+1)^4, (n+2)^5` == [1, 6, 6, 6, 6, 7, 7, 7, 7, 7]
   - `n=7`: 1, `(n)^2, (n+1)^2, (n+2)^7`
   - `n=9`: 1, `(n)^2, (n+1)^2, (n+2)^9`
   - `n=m`: 1, `(n)^2, (n+1)^2, (n+2)^n` (?) Conjecture.
 - `nP * (n-1)P1` not a bad core

# HZ

 - `Δ=4`, K5-e == 2P1 * C3
 - `Δ=5`, 3P1 * C4
 - `Δ=6`, 4P1 * C5, C4 * C3
 - `Δ=7`, 5P1 * C6, C5 * C4, 5P1 * (C3 + C3)
 - `Δ=8`, ...
