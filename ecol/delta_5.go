package main

import "sync"
import "bufio"
import "os"
import "encoding/json"

type Delta5Input struct {
	N        int     `json:"n"`
	Delta    int     `json:"delta"`
	EdgeData [][]int `json:"edge_data"`
}

type Delta5Param struct {
	N     int
	Delta int
	Graph *Graph
}

type Delta5Output struct {
	N        int     `json:"n"`
	Delta    int     `json:"delta"`
	Class    int     `json:"class"`
	EdgeData [][]int `json:"edge_data"`
}

func delta_5_task() {
	MAX_TASKS := 8

	w := bufio.NewWriter(os.Stdout)
	wg := &sync.WaitGroup{}
	wg.Add(MAX_TASKS)
	rg := &sync.WaitGroup{}
	rg.Add(1)
	params := make(chan Delta5Param, MAX_TASKS)
	results := make(chan Delta5Output, MAX_TASKS)

	defer w.Flush()

	// TASK GOROUTINES
	for i := 0; i < MAX_TASKS; i++ {
		go func() {
			for param := range params {
				n := param.N
				G := param.Graph
				edge_data := G.edge_data
				class := 2
				for j := 0; j < 10; j++ {
					g := NewGraph(G.n)
					G.CopyInto(g)
					cg := WrapGraph(g)
					vizing_heuristic(cg)
					edge_data = g.edge_data
					if colours_used(cg) == max_degree(g) {
						class = 1
						break
					}
				}
				if class == 2 {
					results <- Delta5Output{
						N:        n,
						Delta:    param.Delta,
						EdgeData: edge_data,
						Class:    class,
					}
				}
			}
			wg.Done()
		}()
	}

	// OUTPUT GOROUTINE
	go func() {
		enc := json.NewEncoder(w)
		for result := range results {
			enc.Encode(result)
		}
		rg.Done()
	}()

	// READ IN THE INPUT
	r := json.NewDecoder(os.Stdin)
	for {
		p := Delta5Input{}
		if err := r.Decode(&p); err != nil {
			break
		}
		G := NewGraph(len(p.EdgeData))
		G.edge_data = p.EdgeData
		params <- Delta5Param{
			Delta: p.Delta,
			N:     p.N,
			Graph: G,
		}
	}

	close(params)
	wg.Wait()
	close(results)
	rg.Wait()
}
