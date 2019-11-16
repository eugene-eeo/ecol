package main

import "sync"
import "bufio"
import "os"
import "encoding/json"
import "fmt"

type Core3Input struct {
	D        int     `json:"d"`
	J        int     `json:"J"`
	N        int     `json:"n"`
	ClassTwo bool    `json:"expected_class_two"`
	EdgeData [][]int `json:"edge_data"`
}

type Core3Param struct {
	D     int
	J     int
	N     int
	Class int
	Graph *Graph
}

type Core3Output struct {
	D          int  `json:"d"`
	J          int  `json:"j"`
	N          int  `json:"n"`
	VizingOk   bool `json:"vh_ok"`
	CountingOk bool `json:"cg_ok"`
}

func try_prove_class(g *Graph, class int, algorithm func(*ColouringGraph), rounds int) bool {
	delta := max_degree(g)
	for j := 0; j < rounds; j++ {
		h := NewGraph(g.n)
		g.CopyInto(h)
		ch := WrapGraph(h)
		algorithm(ch)
		is_class_one := colours_used(ch) == delta
		if (class == 1 && is_class_one) || (class == 2 && !is_class_one) {
			return true
		}
	}
	return false
}

func core_3_task() {
	MAX_TASKS := 1

	w := bufio.NewWriter(os.Stdout)
	wg := &sync.WaitGroup{}
	wg.Add(MAX_TASKS)
	rg := &sync.WaitGroup{}
	rg.Add(1)
	params := make(chan Core3Param, MAX_TASKS)
	results := make(chan Core3Output, MAX_TASKS)

	defer w.Flush()

	for i := 0; i < MAX_TASKS; i++ {
		go func() {
			for param := range params {
				n := param.N
				G := param.Graph

				vh_ok := try_prove_class(G, param.Class, vizing_heuristic, 20)
				cg_ok := try_prove_class(G, param.Class, counting_heuristic_colour, 20)

				results <- Core3Output{
					N: n, VizingOk: vh_ok, CountingOk: cg_ok,
					D: param.D,
					J: param.J,
				}
			}
			wg.Done()
		}()
	}

	go func() {
		fmt.Fprintln(w, "n,d,j,vh_ok,cg_ok")
		for result := range results {
			a := 1
			b := 1
			if !result.VizingOk {
				a = 0
			}
			if !result.CountingOk {
				b = 0
			}
			fmt.Fprintf(w, "%d,%d,%d,%d,%d\n", result.N, result.D, result.J, a, b)
		}
		rg.Done()
	}()

	r := json.NewDecoder(os.Stdin)
	for {
		p := Core3Input{}
		err := r.Decode(&p)
		if err != nil {
			break
		}
		G := NewGraph(len(p.EdgeData))
		G.edge_data = p.EdgeData
		class := 1
		if p.ClassTwo {
			class = 2
		}
		params <- Core3Param{
			D:     p.D,
			J:     p.J,
			Class: class,
			N:     p.N,
			Graph: G,
		}
	}

	close(params)
	wg.Wait()
	close(results)
	rg.Wait()
}
