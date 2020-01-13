// Utilities for making sure that graphs conform to some
// structures.

package main

import "encoding/json"
import "os"
import "bufio"
import "github.com/willf/bitset"

type EdgeDataOutput struct {
	EdgeData [][]int `json:"edge_data"`
}

type GraphCheckConfig struct {
	DeltaCore int
	Delta     int
	Overfull  bool
	Underfull bool
	Validate  bool
}

type GraphCheckMetadata struct {
	G       *Graph
	Core    *bitset.BitSet
	AdjList []*bitset.BitSet
	Degree  []int
	Delta   int
}

func (gc *GraphCheckMetadata) Alloc() {
	gc.Core = bitset.New(uint(gc.G.n))
	gc.Degree = make([]int, gc.G.n)
	gc.AdjList = make([]*bitset.BitSet, gc.G.n)
	for i, _ := range gc.AdjList {
		gc.AdjList[i] = bitset.New(uint(gc.G.n))
	}
}

func (gc *GraphCheckMetadata) Update() {
	// Clear everything first
	gc.Core.ClearAll()
	for i, bs := range gc.AdjList {
		bs.ClearAll()
		gc.Degree[i] = 0
	}
	// Actually update
	gc.Delta = max_degree(gc.G)
	for u := 0; u < gc.G.n; u++ {
		gc.Degree[u] = gc.G.Degree(u)
		if gc.Degree[u] == gc.Delta {
			gc.Core.Set(uint(u))
		}
		adj := gc.G.edge_data[u]
		for v := 0; v < gc.G.n; v++ {
			if adj[v] != -1 {
				gc.AdjList[u].Set(uint(v))
			}
		}
	}
}

// core_delta checks if the max degree of core = delta
func core_delta(gc *GraphCheckMetadata, target int) bool {
	deg := uint(target)
	for i := 0; i < gc.G.n; i++ {
		if gc.Degree[i] == gc.Delta &&
			gc.Core.IntersectionCardinality(gc.AdjList[i]) > deg {
			return false
		}
	}
	return true
}

// valid_semicore checks if the graph is a valid semicore
func valid_semicore(gc *GraphCheckMetadata) bool {
	for i := 0; i < gc.G.n; i++ {
		if gc.Degree[i] < gc.Delta && gc.Core.IntersectionCardinality(gc.AdjList[i]) == 0 {
			return false
		}
	}
	return true
}

func gc_vm_task(config *VMConfig, gc *GraphCheckMetadata, g *Graph) (int, *Graph) {
	// Construct template graph
	graph := gc.G
	delta := gc.Delta
	class := 2
OUTER:
	for _, algorithm := range config.Algorithms {
		for i := 0; i < config.Attempts; i++ {
			graph.CopyInto(g)
			cg := WrapGraph(g)
			algorithm(cg)
			if colours_used(cg) == delta {
				class = 1
				break OUTER
			}
		}
	}
	return class, g
}

func gc_perform(config *GraphCheckConfig, vmConfig *VMConfig) {
	writer := bufio.NewWriter(os.Stdout)
	encoder := json.NewEncoder(writer)
	scanner := bufio.NewScanner(os.Stdin)

	// Avoid allocations if possible
	g := NewGraph(0)
	h := NewGraph(0)
	gc := &GraphCheckMetadata{G: g}

	for scanner.Scan() {
		data := scanner.Bytes()
		cursor, size := graph6_get_size(data)
		if size != g.n {
			g = NewGraph(size)
			h = NewGraph(size)
			gc.G = g
			gc.Alloc()
		}
		graph6_write_graph(data[cursor:], size, g)
		gc.Update()

		// Validate graph
		if (!config.Validate ||
			(valid_semicore(gc) &&
				gc.Delta == config.Delta &&
				core_delta(gc, config.DeltaCore))) &&
			(!config.Overfull || is_overfull(gc.G)) &&
			(!config.Underfull || !is_overfull(gc.G)) {

			// Emit if we should
			if vmConfig == nil {
				encoder.Encode(EdgeDataOutput{gc.G.edge_data})
				writer.Flush()
			} else {
				class, graph := gc_vm_task(vmConfig, gc, h)
				if class == 2 || vmConfig.EmitClassOne {
					encoder.Encode(EdgeDataOutput{graph.edge_data})
					writer.Flush()
				}
			}
		}
	}
}
