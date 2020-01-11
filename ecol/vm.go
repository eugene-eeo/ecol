package main

import "bufio"
import "sync"
import "os"
import "encoding/json"
import "os/signal"

// Expect edge_data in this input
type VMInput map[string]interface{}

func (vi VMInput) EdgeData() [][]int {
	ed, ok := vi["edge_data"]
	if !ok {
		return nil
	}
	edg := ed.([]interface{})
	edge_data := make([][]int, len(edg))
	for i, row := range edg {
		edge_data[i] = make([]int, len(edg))
		for j, x := range row.([]interface{}) {
			// So we can chain multiple ecol outputs together; we remove all the colouring info
			// and keep just the relevant parts
			v := int(x.(float64))
			if v != -1 {
				v = 0
			}
			edge_data[i][j] = v
		}
	}
	return edge_data
}

type VMConfig struct {
	Tasks        int
	Attempts     int
	UseVH        bool
	UseCH        bool
	UseBF        bool
	EmitClassOne bool
	Algorithms   []func(*ColouringGraph)
}

func (vc *VMConfig) Init() {
	algos := []func(*ColouringGraph){}
	if vc.UseVH {
		algos = append(algos, vizing_heuristic)
	}
	if vc.UseCH {
		algos = append(algos, counting_heuristic_colour)
	}
	if vc.UseBF {
		algos = append(algos, brute_force_colour)
	}
	vc.Algorithms = algos
}

type VMOutput map[string]interface{}

func vm_task(config *VMConfig, input VMInput) VMOutput {
	// Construct template graph
	edge_data := input.EdgeData()
	graph := NewGraph(len(edge_data))
	graph.edge_data = edge_data
	delta := max_degree(graph)
	class := 2

OUTER:
	for _, algorithm := range config.Algorithms {
		for i := 0; i < config.Attempts; i++ {
			g := NewGraph(graph.n)
			graph.CopyInto(g)
			cg := WrapGraph(g)
			algorithm(cg)
			edge_data = cg.g.edge_data
			if colours_used(cg) == delta {
				class = 1
				break OUTER
			}
		}
	}

	if class == 1 && !config.EmitClassOne {
		return nil
	}

	output := VMOutput{}
	for k, v := range input {
		output[k] = v
	}
	output["edge_data"] = edge_data
	output["class"] = class
	return output
}

func vm_perform(config *VMConfig) {
	inputChan := make(chan VMInput, config.Tasks)
	resultsChan := make(chan VMOutput, config.Tasks)

	// Synchronisation
	workersWg := &sync.WaitGroup{}
	workersWg.Add(config.Tasks)
	writerWg := &sync.WaitGroup{}
	writerWg.Add(1)

	// Spawn workers
	for i := 0; i < config.Tasks; i++ {
		go func() {
			for task := range inputChan {
				output := vm_task(config, task)
				if output != nil {
					resultsChan <- output
				}
			}
			workersWg.Done()
		}()
	}

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)

	// Spawn writer
	go func() {
		w := bufio.NewWriter(os.Stdout)
		encoder := json.NewEncoder(w)
		shouldContinue := true
		for shouldContinue {
			select {
			case output, ok := <-resultsChan:
				shouldContinue = ok
				if ok {
					encoder.Encode(output)
				}
			// Wait for interrupt, just flush all output
			case <-c:
				w.Flush()
				os.Exit(1)
			}
		}
		writerWg.Done()
		w.Flush()
	}()

	decoder := json.NewDecoder(os.Stdin)
	for {
		input := VMInput{}
		err := decoder.Decode(&input)
		if err != nil {
			break
		}
		inputChan <- input
	}

	close(inputChan)
	workersWg.Wait()
	close(resultsChan)
	writerWg.Wait()
}
