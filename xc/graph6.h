#ifndef GRAPH6_H
#define GRAPH6_H

#include "graph.h"

typedef struct {
    int cursor;
    int size;
} graph6_state;

graph6_state graph6_get_size(char* data);
void graph6_write_graph(char* data, int cursor, int size, graph* g);

#endif /* GRAPH6_H */
