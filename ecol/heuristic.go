package main

import "github.com/willf/bitset"

func vizing_heuristic(cg *ColouringGraph) {
	delta := uint(max_degree(cg.g))
	colours := bitset.New(delta + 2).Complement()
	colours.SetTo(0, false)
	colours.SetTo(delta+1, false)
	cg.AddColours(colours)

	// 'globals'
	taboo := uint(0)
	w := -1
	v_0 := -1
	beta := uint(0)
	P := allocate_path_array(cg)
	S := bitset.New(delta + 2)

	for len(cg.uncoloured) > 0 {
		if taboo == 0 {
			edge := cg.NextUncolouredEdge()
			w = edge.i
			v_0 = edge.j
		}

		// Don't allocate new bit sets every iteration
		cg.free[v_0].Copy(S)
		S.InPlaceIntersection(cg.free[w])
		if S.Any() {
			colour, _ := S.NextSet(0)
			cg.Set(w, v_0, int(colour))
			taboo = 0
		} else {

			// Check if free[v_0] has some colour != taboo
			cg.free[v_0].Copy(S)
			S.SetTo(taboo, false)

			if S.None() {
				cg.AddColour(delta + 1)
				cg.Set(w, v_0, int(delta+1))
				taboo = 0
			} else {
				a_0, _ := S.NextSet(0)
				if taboo == 0 {
					beta, _ = cg.free[w].NextSet(0)
				}
				P2 := get_path(cg, v_0, int(beta), int(a_0), P)
				if P2[len(P2)-1] != w {
					switch_path(cg, P2, int(beta), int(a_0))
					cg.Set(w, v_0, int(beta))
					taboo = 0
				} else {
					a := P2[len(P2)-2]
					cg.Set(w, a, 0)
					cg.Set(w, v_0, int(a_0))
					v_0 = a
					taboo = a_0
				}
			}
		}
	}
}
