package main

import "os"
import "bufio"
import "fmt"
import "math/rand"
import "sync"

func complete_bipartite_graph(n int, m int) *ColouringGraph {
	g := NewGraph(n + m)
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			g.Set(i, n+j, 0)
			g.Set(n+j, i, 0)
		}
	}
	return WrapGraph(g)
}

func erdos_renyi_into(n int, p float64, seed int64, g *Graph) {
	r := rand.New(rand.NewSource(seed))
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if r.Float64() <= p {
				g.edge_data[i][j] = 0
				g.edge_data[j][i] = 0
			}
		}
	}
}

func erdos_renyi_graph(n int, p float64, seed int64) *Graph {
	g := NewGraph(n)
	erdos_renyi_into(n, p, seed, g)
	return g
}

func complete_graph(k int) *ColouringGraph {
	g := NewGraph(k)
	for i := 0; i < k; i++ {
		for j := i + 1; j < k; j++ {
			g.Set(i, j, 0)
			g.Set(j, i, 0)
		}
	}
	return WrapGraph(g)
}

type ERParams struct {
	n int
	p float64
}

type ERBenchmark struct {
	n               int
	p               float64
	delta           int
	cg_colours_used int
	vh_colours_used int
}

func main() {
	erdos_renyi_test()
}

func erdos_renyi_test() {
	P := []float64{0.125, 0.25, 0.5, 0.75, 0.95}
	R := 5000

	seedsChan := make(chan int64, 8)
	paramsChan := make(chan ERParams, 8)
	resultsChan := make(chan ERBenchmark, 8)
	wg := &sync.WaitGroup{}
	wg.Add(8)

	rg := &sync.WaitGroup{}
	rg.Add(1)

	go func() {
		n := int64(0)
		for {
			n++
			seedsChan <- n
		}
	}()

	for i := 0; i < 8; i++ {
		go func() {
			n_0 := 0
			g_0 := NewGraph(0)
			g_1 := NewGraph(0)
			for param := range paramsChan {
				n := param.n
				p := param.p
				if n == n_0 {
					erdos_renyi_into(n, p, <-seedsChan, g_0)
				} else {
					g_0 = erdos_renyi_graph(n, p, <-seedsChan)
					g_1 = NewGraph(n)
				}
				g_0.CopyInto(g_1)
				g := WrapGraph(g_0)
				h := WrapGraph(g_1)
				vizing_heuristic(g)
				counting_colour(h)
				resultsChan <- ERBenchmark{
					n:               n,
					p:               p,
					delta:           max_degree(g),
					vh_colours_used: colours_used(g),
					cg_colours_used: colours_used(h),
				}
			}
			wg.Done()
		}()
	}

	go func() {
		w := bufio.NewWriter(os.Stdout)
		defer w.Flush()
		fmt.Fprintln(w, "n,p,delta,vh,cg")
		for r := range resultsChan {
			fmt.Fprintf(w, "%d,%f,%d,%d,%d\n", r.n, r.p, r.delta, r.vh_colours_used, r.cg_colours_used)
		}
		rg.Done()
	}()

	for _, p := range P {
		for n := 1; n < 200; n += 5 {
			for i := 0; i < R; i++ {
				paramsChan <- ERParams{n, p}
			}
		}
	}
	close(paramsChan)
	wg.Wait()
	close(resultsChan)
	rg.Wait()
}
