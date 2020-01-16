// Utilities for making sure that graphs conform to some
// structures.

package main

import "encoding/json"
import "os"
import "sync"
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

func (gc *GraphCheckMetadata) Validate(config *GraphCheckConfig) bool {
	if (config.Overfull && !is_overfull(gc.G)) ||
		(config.Underfull && is_overfull(gc.G)) {
		return false
	}
	if !config.Validate {
		return true
	}
	return (config.Delta == 0 || config.Delta == gc.Delta) &&
		valid_semicore(gc) &&
		core_delta(gc, config.DeltaCore)
}

// core_delta checks if the max degree of core = delta
func core_delta(gc *GraphCheckMetadata, target int) bool {
	deg := uint(target)
	max := uint(0)
	for i := 0; i < gc.G.n; i++ {
		if gc.Degree[i] == gc.Delta {
			c_deg := gc.Core.IntersectionCardinality(gc.AdjList[i])
			if c_deg > deg {
				return false
			}
			if c_deg > max {
				max = c_deg
			}
		}
	}
	return max == deg
}

// valid_semicore checks if the graph is a valid semicore
func valid_semicore(gc *GraphCheckMetadata) bool {
	for i := 0; i < gc.G.n; i++ {
		if gc.Core.IntersectionCardinality(gc.AdjList[i]) == 0 {
			return false
		}
	}
	return true
}

func gc_vm_task(config *VMConfig, gc *GraphCheckMetadata) int {
	// Construct template graph
	graph := gc.G
	delta := gc.Delta
	class := 2
	if is_overfull(graph) {
		return 2
	}
OUTER:
	for _, algorithm := range config.Algorithms {
		for i := 0; i < config.Attempts; i++ {
			graph.ResetColours()
			cg := WrapGraph(graph)
			algorithm(cg)
			if colours_used(cg) == delta {
				class = 1
				break OUTER
			}
		}
	}
	return class
}

func gc_perform(config *GraphCheckConfig, vmConfig *VMConfig) {
	scanner := bufio.NewScanner(os.Stdin)

	TASKS := 8
	workerWg := &sync.WaitGroup{}
	workerWg.Add(TASKS)
	writerWg := &sync.WaitGroup{}
	writerWg.Add(1)

	dataChan := make(chan string, 8)
	outChan := make(chan []byte, 8)

	// Worker tasks
	for i := 0; i < TASKS; i++ {
		go func() {
			// Avoid allocations if possible
			g := NewGraph(0)
			gc := &GraphCheckMetadata{G: g}
			for str := range dataChan {
				data := []byte(str)
				cursor, size := graph6_get_size(data)
				if size != g.n {
					g = NewGraph(size)
					gc.G = g
					gc.Alloc()
				}
				graph6_write_graph(data[cursor:], size, g)
				gc.Update()
				// Validate graph
				if !gc.Validate(config) {
					continue
				}
				// Emit if we should
				if vmConfig == nil {
					b, _ := json.Marshal(EdgeDataOutput{gc.G.edge_data})
					outChan <- b
				} else {
					class := gc_vm_task(vmConfig, gc)
					if class == 2 || vmConfig.EmitClassOne {
						b, _ := json.Marshal(EdgeDataOutput{gc.G.edge_data})
						outChan <- b
					}
				}
			}
			workerWg.Done()
		}()
	}

	go func() {
		for jsonData := range outChan {
			os.Stdout.Write(jsonData)
			os.Stdout.Write([]byte("\n"))
		}
		writerWg.Done()
	}()

	for scanner.Scan() {
		dataChan <- scanner.Text()
	}
	close(dataChan)
	workerWg.Wait()
	close(outChan)
	writerWg.Wait()
}
