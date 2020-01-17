CC=gcc
CFLAGS= -std=c99 -Ofast -march=native -finline-functions -flto -funroll-loops
DEBUG_CFLAGS= -std=c99 -O0 -march=native -g

all: xc_ gc_

debug:
	$(CC) $(DEBUG_CFLAGS) -o xc xc.c graph.c bitset.c vizing_heuristic.c graph6.c
	$(CC) $(DEBUG_CFLAGS) -o gc graphcheck.c graph.c bitset.c graph6.c

xc_:
	$(CC) $(CFLAGS) -o xc xc.c graph.c bitset.c vizing_heuristic.c graph6.c

gc_:
	$(CC) $(CFLAGS) -o gc graphcheck.c graph.c bitset.c graph6.c
