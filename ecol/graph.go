package main

type Graph struct {
	n         int
	edge_data [][]int
}

type Edge struct {
	i int
	j int
}

func NewGraph(n int) *Graph {
	edge_data := make([][]int, n)
	for i := 0; i < n; i++ {
		edge_data[i] = make([]int, n)
		for j := 0; j < n; j++ {
			edge_data[i][j] = -1
		}
	}
	return &Graph{n, edge_data}
}

func (g *Graph) Get(i, j int) int {
	return g.edge_data[i][j]
}

func (g *Graph) Set(i, j, v int) {
	g.edge_data[i][j] = v
	g.edge_data[j][i] = v
}

func (g *Graph) Edges() []Edge {
	edges := []Edge{}
	for i := 0; i < g.n; i++ {
		for j := i; j < g.n; j++ {
			if g.edge_data[i][j] != -1 {
				edges = append(edges, Edge{i, j})
			}
		}
	}
	return edges
}

func (g *Graph) Degree(u int) int {
	d := 0
	for i := 0; i < g.n; i++ {
		if g.edge_data[u][i] != -1 {
			d++
		}
	}
	return d
}

func (g *Graph) Neighbours(u int) []int {
	N := []int{}
	for i := 0; i < g.n; i++ {
		if g.edge_data[u][i] != -1 {
			N = append(N, i)
		}
	}
	return N
}

func (g *Graph) CopyInto(h *Graph) {
	for i, x := range g.edge_data {
		for j, v := range x {
			h.edge_data[i][j] = v
		}
	}
}
