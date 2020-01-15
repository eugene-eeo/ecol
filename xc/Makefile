CC=gcc
CFLAGS= -std=c99 -O3 -g

all: xc clean

xc: deps
	${CC} $(CFLAGS) -o xc main.o graph.o bitset.o vizing_heuristic.o graph6.o

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

deps: graph.o bitset.o vizing_heuristic.o graph6.o main.o

clean:
	-rm *.o
