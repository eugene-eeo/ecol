all:
	gcc -c -g graph.c
	gcc -c -g bitset.c
	gcc -c -g vizing_heuristic.c
	gcc -c -g main.c
	gcc -o main main.o graph.o bitset.o vizing_heuristic.o

clean:
	rm *.o
