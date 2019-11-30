package main

import "github.com/willf/bitset"

type ColouringGraph struct {
	g          *Graph
	free       []*bitset.BitSet
	uncoloured map[Edge]bool
}

func WrapGraph(g *Graph) *ColouringGraph {
	uncoloured := map[Edge]bool{}
	for _, edge := range g.Edges() {
		uncoloured[edge] = true
	}
	cg := &ColouringGraph{
		g:          g,
		free:       nil,
		uncoloured: uncoloured,
	}
	delta := max_degree(cg.g)
	free := make([]*bitset.BitSet, g.n)
	for i := 0; i < g.n; i++ {
		free[i] = bitset.New(uint(delta + 2))
	}
	cg.free = free
	return cg
}

func (cg *ColouringGraph) AddColour(colour uint) {
	for _, b := range cg.free {
		b.Set(colour)
	}
}

func (cg *ColouringGraph) AddColours(colours *bitset.BitSet) {
	for _, b := range cg.free {
		b.InPlaceUnion(colours)
	}
}

func (cg *ColouringGraph) Get(i, j int) int {
	return cg.g.Get(i, j)
}

func (cg *ColouringGraph) Set(i, j, v int) {
	// Maintain that i <= j
	if i > j {
		i, j = j, i
	}
	og := cg.Get(i, j)
	if og != 0 {
		cg.free[i].SetTo(uint(og), true)
		cg.free[j].SetTo(uint(og), true)
	}
	if v == 0 {
		cg.uncoloured[Edge{i, j}] = true
	} else {
		cg.free[i].SetTo(uint(v), false)
		cg.free[j].SetTo(uint(v), false)
		delete(cg.uncoloured, Edge{i, j})
	}
	cg.g.Set(i, j, v)
}

func (cg *ColouringGraph) NextUncolouredEdge() Edge {
	for k := range cg.uncoloured {
		return k
	}
	return Edge{-1, -1}
}

// Utility functions

func find_endpoint_with_colour_subset(cg *ColouringGraph, u int, colour int, limit int) int {
	row := cg.g.edge_data[u]
	for i := 0; i <= limit; i++ {
		if i != u && row[i] == colour {
			return i
		}
	}
	return -1
}

func get_path_subset(cg *ColouringGraph, v int, alpha, beta int, path []int, limit int) []int {
	path[0] = v
	swatch := [2]int{beta, alpha}
	length := 1
	for {
		endpoint := find_endpoint_with_colour_subset(cg, path[length-1], swatch[length%2], limit)
		if endpoint == -1 {
			break
		}
		path[length] = endpoint
		length++
	}
	return path[:length]
}

func find_endpoint_with_colour(cg *ColouringGraph, u int, colour int) int {
	row := cg.g.edge_data[u]
	for i := 0; i < u; i++ {
		if row[i] == colour {
			return i
		}
	}
	for i := u + 1; i < cg.g.n; i++ {
		if row[i] == colour {
			return i
		}
	}
	return -1
}

func allocate_path_array(cg *ColouringGraph) []int {
	return make([]int, cg.g.n)
}

func get_path(cg *ColouringGraph, v int, alpha, beta int, path []int) []int {
	path[0] = v
	swatch := [2]int{beta, alpha}
	length := 1
	for {
		endpoint := find_endpoint_with_colour(cg, path[length-1], swatch[length%2])
		if endpoint == -1 {
			break
		}
		path[length] = endpoint
		length++
	}
	return path[:length]
}

func switch_path(cg *ColouringGraph, path []int, alpha, beta int) {
	for i := 0; i < len(path)-1; i++ {
		cg.Set(path[i], path[i+1], 0)
	}
	swatch := [2]int{beta, alpha}
	for i := 0; i < len(path)-1; i++ {
		cg.Set(path[i], path[i+1], swatch[i%2])
	}
}

func max_degree(g *Graph) int {
	max := 0
	for i := 0; i < g.n; i++ {
		d := g.Degree(i)
		if d > max {
			max = d
		}
	}
	return max
}

func colours_used(cg *ColouringGraph) int {
	colours := bitset.New(uint(max_degree(cg.g)))
	for _, e := range cg.g.Edges() {
		colours.Set(uint(cg.Get(e.i, e.j)))
	}
	return int(colours.Count())
}

func validate_colouring(g *Graph) bool {
	for i := 0; i < g.n; i++ {
		x := bitset.New(0)
		for j := 0; j < g.n; j++ {
			if i != j && g.edge_data[i][j] != -1 {
				x.Set(uint(g.edge_data[i][j]))
			}
		}
		if x.Count() != uint(g.Degree(i)) {
			return false
		}
	}
	return true
}

func is_overfull(g *Graph) bool {
	return g.EdgeCount() > max_degree(g)*(g.n/2)
}

func core_size(g *Graph) int {
	delta := max_degree(g)
	num := 0
	for i := 0; i < g.n; i++ {
		if g.Degree(i) == delta {
			num++
		}
	}
	return num
}
