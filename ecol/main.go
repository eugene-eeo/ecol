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

	is_vm := flag.Bool("vm", false, "vm mode")
	is_gc := flag.Bool("gc", false, "gc mode")

	// VM FLAGS
	tasks := flag.Int("tasks", 8, "number of tasks")
	attempts := flag.Int("attempts", 20, "number of attempts")
	use_vh := flag.Bool("use-vh", true, "use vizing heuristic")
	use_ch := flag.Bool("use-ch", true, "use counting heuristic")
	emit_class_one := flag.Bool("emit-class-one", false, "emit class one graphs")

	// GC FLAGS
	validate := flag.Bool("validate", true, "perform semicore, delta-core, and delta checks")
	delta_core := flag.Int("delta-core", 2, "delta core")
	delta := flag.Int("delta", 5, "delta")
	overfull := flag.Bool("overfull", false, "overfull")
	underfull := flag.Bool("underfull", false, "underfull")

	flag.Parse()

	if *is_gc {
		// GC mode
		config := &GraphCheckConfig{
			Delta:     *delta,
			DeltaCore: *delta_core,
			Overfull:  *overfull,
			Underfull: *underfull,
			Validate:  *validate,
		}
		var vmConfig *VMConfig = nil
		if *is_vm {
			vmConfig = &VMConfig{
				Tasks:        *tasks,
				Attempts:     *attempts,
				UseVH:        *use_vh,
				UseCH:        *use_ch,
				UseBF:        false,
				EmitClassOne: *emit_class_one,
			}
			vmConfig.Init()
		}
		gc_perform(config, vmConfig)
		return
	}
	if *is_vm {
		// VM mode
		config := &VMConfig{
			Tasks:        *tasks,
			Attempts:     *attempts,
			UseVH:        *use_vh,
			UseCH:        *use_ch,
			UseBF:        false,
			EmitClassOne: *emit_class_one,
		}
		config.Init()
		vm_perform(config)
	}
}
