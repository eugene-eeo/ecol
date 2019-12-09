package main

import "github.com/willf/bitset"

func unique_values(p []int) int {
	bs := bitset.New(1)
	for _, x := range p {
		bs.Set(uint(x))
	}
	return int(bs.Count())
}

// NextIndex sets ix to the lexicographically next value,
// such that for each i>0, 0 <= ix[i] < lens.
func NextIndex(ix []int, lens int) {
	for j := len(ix) - 1; j >= 0; j-- {
		ix[j]++
		if j == 0 || ix[j] < lens {
			return
		}
		ix[j] = 0
	}
}

// Build an adjacency list
func build_adj_list(edges []Edge) [][2]Edge {
	adjList := [][2]Edge{}
	n := len(edges)
	for i, uv := range edges {
		for j := i + 1; j < n; j++ {
			st := edges[j]
			if uv.i == st.i || uv.i == st.j || uv.j == st.i || uv.j == st.j {
				adjList = append(adjList, [2]Edge{uv, st})
			}
		}
	}
	return adjList
}

func fast_valid_edge_colouring(g *Graph, adjList [][2]Edge) bool {
	for _, adj := range adjList {
		ab := adj[0]
		cd := adj[1]
		if g.edge_data[ab.i][ab.j] == g.edge_data[cd.i][cd.j] {
			return false
		}
	}
	return true
}

// brute_force_colour does brute force colouring on the graph
func brute_force_colour(cg *ColouringGraph) {
	// We don't need the ColouringGraph machinery here,
	// it will only slow us down if anything...
	graph := cg.g
	delta := max_degree(graph)
	colours := delta + 1

	edges := graph.Edges()
	adjList := build_adj_list(edges)
	n := graph.EdgeCount()

	best_num := delta + 2
	best_col := make([]int, n)

OUTER:
	for p := make([]int, n); p[0] < colours; NextIndex(p, colours) {
		for idx, edge := range edges {
			graph.Set(edge.i, edge.j, p[idx]+1)
		}
		if fast_valid_edge_colouring(graph, adjList) {
			num := unique_values(p)
			if num < best_num {
				best_num = num
				copy(best_col, p)
				if best_num == delta {
					break OUTER
				}
			}
		}
	}

	for i, colour := range best_col {
		edge := edges[i]
		cg.Set(edge.i, edge.j, colour)
	}
}
