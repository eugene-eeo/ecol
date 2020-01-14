all: clean deps
	gcc -O3 -o xc main.o graph.o bitset.o vizing_heuristic.o graph6.o

debug: deps
	gcc -O3 -g -o xc main.o graph.o bitset.o vizing_heuristic.o graph6.o

deps:
	gcc -c -g graph.c
	gcc -c -g bitset.c
	gcc -c -g vizing_heuristic.c
	gcc -c -g graph6.c
	gcc -c -g main.c

clean:
	rm *.o
