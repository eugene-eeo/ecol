#ifndef GRAPH6_H
#define GRAPH6_H

#include "graph.h"

typedef struct {
    int cursor;
    int size;
} graph6_state;

// read
graph6_state graph6_get_size(char* data);
void graph6_read_graph(char* data, int cursor, int size, graph* g);

// write
int graph6_get_bytes_needed(int n);
void graph6_write_bytes(graph g, int n, char* buf);

#endif /* GRAPH6_H */
