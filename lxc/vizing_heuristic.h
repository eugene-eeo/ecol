#ifndef VIZING_H
#define VIZING_H

#include "graph.h"
#include "bitset.h"

int vizing_heuristic(graph* g, int* P, int delta, bitset* S, int full);

#endif /* VIZING_H */
