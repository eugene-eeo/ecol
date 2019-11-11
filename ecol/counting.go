package main

import "github.com/willf/bitset"

func counting_colour(G *ColouringGraph) {
	delta := uint(max_degree(G.g))
	colours := bitset.New(delta + 2).Complement()
	colours.SetTo(0, false)
	G.AddColours(colours)
	max_size := delta + 2

	P := allocate_path_array(G)
	C := bitset.New(uint(G.g.n)) // Used to compute F(uv_1) U F(uv_2) U ...
	F := bitset.New(uint(G.g.n)) // Used to compute F(u) \ C
	N := 0
	var f_u *bitset.BitSet = nil
	var r []int = nil

	F_u := make(map[int]*FreesetInfo, G.g.n)
	// Use this to populate F_u to avoid reallocs
	fsets := make([]*FreesetInfo, G.g.n)
	for i := range fsets {
		fsets[i] = &FreesetInfo{bitset.New(delta + 2), 0}
	}

	for u := 0; u < G.g.n; u++ {
		// u := current node to colour
		// All nodes < u is in V, so we don't have to store it in a set
		// W is implicitly captured in keys of F_u
		N = 0
		f_u = G.free[u]
		r = G.g.edge_data[u]
		// Compute F_u[x] = F(ux) = F(u) & F(x)
		for v := 0; v < u; v++ {
			if r[v] == 0 {
				N++
				fi := fsets[v]
				f_u.Copy(fi.fset)
				fi.fset.InPlaceIntersection(G.free[v])
				fi.size = fi.fset.Count()
				F_u[v] = fi
			}
		}
	OUTER:
		for n := 0; n < N; n++ {
			// Compute union of all F(uv) (v in W)
			C.ClearAll()
			for _, fi := range F_u {
				C.InPlaceUnion(fi.fset)
			}

			for l, e := C.NextSet(0); e; l, e = C.NextSet(l + 1) {
				v := 0            // v s.t. |F_uv| is minimum
				c_min := max_size // Minimum size of F_uv
				count := 0        // Count of |F_uv| <= 2
				for z, fi := range F_u {
					if fi.fset.Test(l) {
						if fi.size <= 2 {
							count++
						}
						if fi.size <= c_min {
							c_min = fi.size
							v = z
						}
					}
				}
				// Case (1)
				if count <= 1 {
					G.Set(u, v, int(l))
					delete(F_u, v)
					for _, fi := range F_u {
						if fi.fset.Test(l) {
							fi.fset.SetTo(l, false)
							fi.size--
						}
					}
					continue OUTER
				}
			}

			// Case (2)
			G.free[u].Copy(F)
			F.InPlaceDifference(C)
			b, _ := F.NextSet(0)
			w := 0
			best_size := max_size
			for v, fi := range F_u {
				if fi.size <= best_size {
					w = v
					best_size = fi.size
				}
			}
			a, _ := F_u[w].fset.NextSet(0)

			// Switch G[0..u][a,b]
			bc := int(b)
			ac := int(a)
			P2 := get_path_subset(G, w, bc, ac, P, u)
			switch_path(G, P2, bc, ac)
			G.Set(u, w, bc)
			// Update F_u
			delete(F_u, w)
			// If P2[-1] in W
			if fi, ok := F_u[P2[len(P2)-1]]; ok {
				fi.fset.SetTo(a, false)
				fi.size--
			}
		}
	}
}
