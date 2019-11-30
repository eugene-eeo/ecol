package main

import "flag"

func main() {
	// for n := 0; n <= 200; n++ {
	// 	G := complete_graph(n)
	// 	vizing_heuristic(G)
	// 	if !validate_colouring(G) {
	// 		fmt.Println("FAIL", n)
	// 		break
	// 	}
	// 	H := complete_graph(n)
	// 	counting_heuristic_colour(H)
	// 	if !validate_colouring(H) {
	// 		fmt.Println("FAIL", n)
	// 		break
	// 	}
	// }
	tasks := flag.Int("tasks", 8, "number of tasks")
	attempts := flag.Int("attempts", 20, "number of attempts")
	use_vh := flag.Bool("use-vh", true, "use vizing heuristic")
	use_ch := flag.Bool("use-ch", true, "use counting heuristic")
	emit_class_one := flag.Bool("emit-class-one", false, "emit class one graphs")
	flag.Parse()

	config := VMConfig{
		Tasks:        *tasks,
		Attempts:     *attempts,
		UseVH:        *use_vh,
		UseCH:        *use_ch,
		EmitClassOne: *emit_class_one,
	}
	vm_perform(&config)
}
