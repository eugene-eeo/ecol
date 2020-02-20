CC=gcc
CFLAGS= -std=c99 -Ofast -march=native -funroll-loops -mbmi2
DEBUG_CFLAGS= -std=c99 -O0 -march=native -g -mbmi2

all: _lxc

check:
	cppcheck *.c *.h

_lxc:
	$(CC) $(CFLAGS) -o lxc lxc.c graph.c bitset.c vizing_heuristic.c graph6.c

debug:
	$(CC) $(DEBUG_CFLAGS) -o lxc lxc.c graph.c bitset.c vizing_heuristic.c graph6.c
