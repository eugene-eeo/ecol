CC=gcc
CFLAGS= -std=c18 -Ofast -march=native -finline-functions -flto -funroll-loops
XC_CFLAGS= -D 'XC_GRAPH_COLOUR=1'
DEBUG_CFLAGS= -std=c99 -O0 -march=native -g

all: xc_ gc_ resmod_ cg_

debug:
	$(CC) $(DEBUG_CFLAGS) $(XC_CFLAGS) -o xc xc.c graph.c bitset.c vizing_heuristic.c graph6.c
	$(CC) $(DEBUG_CFLAGS) -o gc gc.c graph.c bitset.c graph6.c
	$(CC) $(DEBUG_CFLAGS) -o cg cg.c graph.c bitset.c graph6.c
	$(CC) $(DEBUG_CFLAGS) -o resmod resmod.c

xc_:
	$(CC) $(CFLAGS) $(XC_CFLAGS) -o xc xc.c graph.c bitset.c vizing_heuristic.c graph6.c

gc_:
	$(CC) $(CFLAGS) -o gc gc.c graph.c bitset.c graph6.c

cg_:
	$(CC) $(CFLAGS) -o cg cg.c graph.c bitset.c graph6.c

resmod_:
	$(CC) $(CFLAGS) -o resmod resmod.c
