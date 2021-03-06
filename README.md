# Edge Colouring

| folder   | description                                             |
|:---------|:------------------------------------------------------- |
| `pyecol` | python implementation of heuristics + some utilities    |
| `ecol`   | go implementation of CB/VH heuristics + graph checking  |
| `xc`     | VH + many utilities implemented in C                    |
| `lxc`    | VH implementation for arbitrary graphs                  |

## Prerequisites

Need to download [nauty](http://users.cecs.anu.edu.au/~bdm/nauty/).

    $ pip install --editable .
    $ pip install -r requirements.txt


## Building

    $ make


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

## Bad cores

 - `nP1 * C(n+1)` (for all n >= 3), hard to identify common substructure.
 - **`K_n`** (even n, n >= 4) is always bad core -- found an edge-critical and vertex-critical (minimal) extension.
 - `K_n` (odd n, n >= 5) is always bad core (but can't find common substructure),
 but degree sequence looks like:
   - `n=5`: `1, (n+1)^4, (n+2)^5` == [1, 6, 6, 6, 6, 7, 7, 7, 7, 7]
   - `n=7`: `1, (n)^2, (n+1)^2, (n+2)^7`
   - `n=9`: `1, (n)^2, (n+1)^2, (n+2)^9`
   - `n=m`: `1, (n)^2, (n+1)^2, (n+2)^n` (?) Conjecture.

## HZ

 - `Δ=4`, K5-e == 2P1 * C3
 - `Δ=5`, 3P1 * C4
 - `Δ=6`, 4P1 * C5, C4 * C3
 - `Δ=7`, 5P1 * C6, C5 * C4, 5P1 * (C3 + C3)
 - `Δ=8`, ...

### `lxc` benchmarks

| name            |     n |   edges |   Δ |   vh |   time |
|:----------------|------:|--------:|----:|-----:|-------:|
| 4-FullIns_4     |   690 |    6650 | 119 |  119 |   0.00 |
| 5-FullIns_4     |  1085 |   11395 | 160 |  160 |   0.00 |
| DSJC500.1       |   500 |   12458 |  68 |   68 |   0.00 |
| anna            |   138 |     493 |  71 |   71 |   0    |
| ash331GPIA      |   662 |    4181 |  23 |   23 |   0.00 |
| ash958GPIA      |  1916 |   12506 |  24 |   24 |   0.02 |
| david           |    87 |     406 |  82 |   82 |   0    |
| games120        |   120 |     638 |  13 |   13 |   0    |
| latin_square_10 |   900 |  307350 | 683 |  **684** |   0.18 |
| le450_15a       |   450 |    8168 |  99 |   99 |   0.00 |
| le450_15b       |   450 |    8169 |  94 |   94 |   0.00 |
| le450_15c       |   450 |   16680 | 139 |  139 |   0.00 |
| le450_15d       |   450 |   16750 | 138 |  138 |   0.00 |
| le450_25a       |   450 |    8260 | 128 |  128 |   0.00 |
| le450_25b       |   450 |    8263 | 111 |  111 |   0.00 |
| le450_25c       |   450 |   17343 | 179 |  179 |   0.00 |
| le450_25d       |   450 |   17425 | 157 |  157 |   0.00 |
| le450_5a        |   450 |    5714 |  42 |   42 |   0.00 |
| le450_5b        |   450 |    5734 |  42 |   42 |   0.00 |
| le450_5c        |   450 |    9803 |  66 |   66 |   0.00 |
| le450_5d        |   450 |    9757 |  68 |   68 |   0.00 |
| miles1000       |   128 |    3216 |  86 |   86 |   0    |
| miles1500       |   128 |    5198 | 106 |  106 |   0    |
| miles500        |   128 |    1170 |  38 |   38 |   0    |
| myciel3         |    11 |      20 |   5 |    5 |   0    |
| myciel4         |    23 |      71 |  11 |   11 |   0    |
| myciel5         |    47 |     236 |  23 |   23 |   0    |
| myciel6         |    95 |     755 |  47 |   47 |   0    |
| myciel7         |   191 |    2360 |  95 |   95 |   0    |
| qg.order30      |   900 |   26100 |  58 |   59 |   0.02 |
| qg.order60      |  3600 |  212400 | 118 |  **119** |   0.68 |
| qg.order100     | 10000 |  990000 | 198 |  **199** | 21.30  |
| queen11_11      |   121 |    1980 |  40 |   40 |   0    |
| queen12_12      |   144 |    2596 |  43 |   43 |   0    |
| queen13_13      |   169 |    3328 |  48 |   48 |   0    |
| queen14_14      |   196 |    4186 |  51 |   51 |   0    |
| queen15_15      |   225 |    5180 |  56 |   56 |   0    |
| queen16_16      |   256 |    6320 |  59 |   59 |   0    |
| wap04a          |  5231 |  294902 | 351 |  351 |   0.75 |
| will199GPIA     |   701 |    6772 |  38 |   38 |   0.00 |
