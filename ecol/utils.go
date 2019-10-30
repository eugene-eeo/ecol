package main

import "fmt"
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
	delta := max_degree(cg)
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

func find_endpoint_with_colour(cg *ColouringGraph, u int, colour int, prev int) int {
	for i := 0; i < cg.g.n; i++ {
		e := cg.g.edge_data[u][i]
		if e == colour && i != prev {
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
	prev := -1
	swatch := [2]int{beta, alpha}
	length := 1
	for {
		endpoint := find_endpoint_with_colour(cg, path[length-1], swatch[length%2], prev)
		if endpoint == -1 {
			break
		}
		prev = path[length-1]
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

func max_degree(cg *ColouringGraph) int {
	max := 0
	for i := 0; i < cg.g.n; i++ {
		d := cg.g.Degree(i)
		if d > max {
			max = d
		}
	}
	return max
}

func colours_used(cg *ColouringGraph) int {
	colours := bitset.New(uint(max_degree(cg)))
	for _, e := range cg.g.Edges() {
		colours.Set(uint(cg.Get(e.i, e.j)))
	}
	return int(colours.Count())
}

func validate_colouring(cg *ColouringGraph) bool {
	for i := 0; i < cg.g.n; i++ {
		x := bitset.New(0)
		for j := 0; j < cg.g.n; j++ {
			if i != j && cg.g.edge_data[i][j] != -1 {
				x.Set(uint(cg.g.edge_data[i][j]))
			}
		}
		if x.Count() != uint(cg.g.Degree(i)) {
			fmt.Println("=================")
			fmt.Println("Invalid")
			fmt.Println(i)
			fmt.Println(cg.g.edge_data[i])
			return false
		}
	}
	return true
}