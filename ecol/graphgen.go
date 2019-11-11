package main

import "sync"
import "bufio"
import "os"
import "encoding/json"

type GraphGenInput struct {
	K        int     `json:"k"`
	N        int     `json:"n"`
	EdgeData [][]int `json:"edge_data"`
}

type GraphGenParam struct {
	k     int
	n     int
	Graph *Graph
}

type GraphGenOutput struct {
	K        int     `json:"k"`
	N        int     `json:"n"`
	EdgeData [][]int `json:"edge_data"`
	ClassOne bool    `json:"is_class_one"`
}

func graph_gen_task() {
	MAX_TASKS := 8

	w := bufio.NewWriter(os.Stdout)
	wg := &sync.WaitGroup{}
	wg.Add(MAX_TASKS)
	rg := &sync.WaitGroup{}
	rg.Add(1)
	params := make(chan GraphGenParam, MAX_TASKS)
	results := make(chan GraphGenOutput, MAX_TASKS)

	defer w.Flush()

	for i := 0; i < 8; i++ {
		go func() {
			for param := range params {
				k := param.k
				n := param.n
				G := param.Graph
				cg := WrapGraph(G)
				vizing_heuristic(cg)
				is_class_one := colours_used(cg) == max_degree(G)
				results <- GraphGenOutput{
					K:        k,
					N:        n,
					EdgeData: G.edge_data,
					ClassOne: is_class_one,
				}
			}
			wg.Done()
		}()
	}

	go func() {
		enc := json.NewEncoder(w)
		for result := range results {
			enc.Encode(result)
		}
		rg.Done()
	}()

	r := json.NewDecoder(os.Stdin)
	for {
		p := GraphGenInput{}
		err := r.Decode(&p)
		if err != nil {
			break
		}
		G := NewGraph(p.K + p.N)
		G.edge_data = p.EdgeData
		params <- GraphGenParam{
			k:     p.K,
			n:     p.N,
			Graph: G,
		}
	}

	close(params)
	wg.Wait()
	close(results)
	rg.Wait()
}
