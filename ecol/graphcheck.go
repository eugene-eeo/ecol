// Utilities for making sure that graphs conform to some
// structures.

package main

import "encoding/json"
import "os"
import "bufio"
import "github.com/willf/bitset"

type GraphCheckConfig struct {
	DeltaCore int
	Delta     int
	Overfull  bool
	Underfull bool
}

type GraphCheckMetadata struct {
	G       *Graph
	Core    *bitset.BitSet
	AdjList []*bitset.BitSet
	Degree  []int
	Delta   int
}

func NewGraphCheckMetadata(G *Graph) *GraphCheckMetadata {
	core := bitset.New(uint(G.n))
	adjList := make([]*bitset.BitSet, G.n)
	degree := make([]int, G.n)
	delta := max_degree(G)

	for u := 0; u < G.n; u++ {
		degree[u] = G.Degree(u)
		if degree[u] == delta {
			core.Set(uint(u))
		}
		adj := G.edge_data[u]
		adjList[u] = bitset.New(uint(G.n))
		for v := 0; v < G.n; v++ {
			if adj[v] != -1 {
				adjList[u].Set(uint(v))
			}
		}
	}

	return &GraphCheckMetadata{
		G:       G,
		Core:    core,
		AdjList: adjList,
		Degree:  degree,
		Delta:   delta,
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

func gc_perform(config *GraphCheckConfig) {
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	encoder := json.NewEncoder(writer)
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		data := scanner.Bytes()
		gc := NewGraphCheckMetadata(ParseGraph6Bytes(data))
		if valid_semicore(gc) &&
			gc.Delta == config.Delta &&
			core_delta(gc, config.DeltaCore) &&
			(!config.Overfull || is_overfull(gc.G)) &&
			(!config.Underfull || !is_overfull(gc.G)) {
			encoder.Encode(map[string][][]int{"edge_data": gc.G.edge_data})
		}
	}
}
