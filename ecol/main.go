package main

import "fmt"
import "math/rand"
import "time"
import "sync"

func erdos_renyi_graph(n int, p float64) *ColouringGraph {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	g := NewGraph(n)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if r.Float64() <= p {
				g.Set(i, j, 0)
			}
		}
	}
	return WrapGraph(g)
}

func complete_graph(k int) *ColouringGraph {
	g := NewGraph(k)
	for i := 0; i < k; i++ {
		for j := i + 1; j < k; j++ {
			g.Set(i, j, 0)
		}
	}
	return WrapGraph(g)
}

type Params struct {
	n int
	p float64
}

type Result struct {
	n            int
	p            float64
	delta        int
	colours_used int
}

func main() {
	P := []float64{0.125, 0.25, 0.5, 0.75, 0.95}
	R := 5000

	paramsChan := make(chan Params, 8)
	resultsChan := make(chan Result, 8)
	wg := &sync.WaitGroup{}
	wg.Add(8)

	rg := &sync.WaitGroup{}
	rg.Add(1)

	for i := 0; i < 8; i++ {
		go func() {
			for param := range paramsChan {
				n := param.n
				p := param.p
				g := erdos_renyi_graph(n, p)
				vizing_heuristic(g)
				resultsChan <- Result{n, p, max_degree(g), colours_used(g)}
			}
			wg.Done()
		}()
	}

	go func() {
		fmt.Println("n,p,delta,colours_used")
		for r := range resultsChan {
			fmt.Printf("%d,%f,%d,%d\n", r.n, r.p, r.delta, r.colours_used)
		}
		rg.Done()
	}()

	for _, p := range P {
		for n := 1; n < 200; n += 5 {
			for i := 0; i < R; i++ {
				paramsChan <- Params{n, p}
			}
		}
	}
	close(paramsChan)
	wg.Wait()
	close(resultsChan)
	rg.Wait()
}
