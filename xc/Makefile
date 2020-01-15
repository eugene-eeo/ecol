CC=gcc
CFLAGS= -std=c99 -O3 -march=native

all: xc clean

xc: deps
	${CC} $(CFLAGS) -o xc xc.o graph.o bitset.o vizing_heuristic.o graph6.o

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

deps: graph.o bitset.o vizing_heuristic.o graph6.o xc.o

clean:
	-rm *.o
