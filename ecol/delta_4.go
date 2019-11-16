package main

import "sync"
import "bufio"
import "os"
import "encoding/json"
import "fmt"

type Delta4Input struct {
	N        int     `json:"n"`
	Delta    int     `json:"delta"`
	Class    int     `json:"class"`
	EdgeData [][]int `json:"edge_data"`
}

type Delta4Param struct {
	N     int
	Delta int
	Class int
	Graph *Graph
}

type Delta4Output struct {
	N            int
	Delta        int
	VizingProb   float64
	CountingProb float64
}

func count_classifications(g *Graph, class int, algorithm func(*ColouringGraph), rounds int) float64 {
	delta := max_degree(g)
	n := 0
	for j := 0; j < rounds; j++ {
		h := NewGraph(g.n)
		g.CopyInto(h)
		ch := WrapGraph(h)
		algorithm(ch)
		is_class_one := colours_used(ch) == delta
		if (class == 1 && is_class_one) || (class == 2 && !is_class_one) {
			n++
		}
	}
	return float64(n) / float64(rounds)
}

func delta_4_task() {
	MAX_TASKS := 8

	w := bufio.NewWriter(os.Stdout)
	wg := &sync.WaitGroup{}
	wg.Add(MAX_TASKS)
	rg := &sync.WaitGroup{}
	rg.Add(1)
	params := make(chan Delta4Param, MAX_TASKS)
	results := make(chan Delta4Output, MAX_TASKS)

	defer w.Flush()

	for i := 0; i < MAX_TASKS; i++ {
		go func() {
			for param := range params {
				n := param.N
				G := param.Graph
				vh_count := count_classifications(G, param.Class, vizing_heuristic, 10)
				cg_count := count_classifications(G, param.Class, counting_heuristic_colour, 10)

				results <- Delta4Output{
					N:            n,
					Delta:        param.Delta,
					VizingProb:   vh_count,
					CountingProb: cg_count,
				}
			}
			wg.Done()
		}()
	}

	go func() {
		fmt.Fprintln(w, "n,delta,vh_prob,cg_prob")
		for result := range results {
			fmt.Fprintf(w, "%d,%d,%f,%f\n", result.N, result.Delta, result.VizingProb, result.CountingProb)
		}
		rg.Done()
	}()

	r := json.NewDecoder(os.Stdin)
	for {
		p := Delta4Input{}
		err := r.Decode(&p)
		if err != nil {
			break
		}
		G := NewGraph(len(p.EdgeData))
		G.edge_data = p.EdgeData
		params <- Delta4Param{
			Class: p.Class,
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
