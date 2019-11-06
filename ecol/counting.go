package main

import "github.com/willf/bitset"

func counting_colour(G *ColouringGraph) {
	delta := uint(max_degree(G))
	colours := bitset.New(delta + 2)
	for i := uint(1); i <= delta+1; i++ {
		colours.Set(i)
	}
	G.AddColours(colours)
	max_size := delta + 2

	P := allocate_path_array(G)
	C := bitset.New(uint(G.g.n))
	F := bitset.New(uint(G.g.n))
	F_u := make(map[uint]*bitset.BitSet, G.g.n)

	for u := 0; u < G.g.n; u++ {
		// u := current node to colour
		// Compute F_u[x] = F(ux) = F(u) & F(x)
		// Everything up to u is in V
		for v := 0; v < u; v++ {
			if G.g.edge_data[u][v] == 0 {
				F_u[uint(v)] = G.free[u].Intersection(G.free[v])
			}
		}
		for len(F_u) > 0 {
			// Compute union of all F(uv) (v in W)
			C.ClearAll()
			for _, v := range F_u {
				C.InPlaceUnion(v)
			}

			found := false
			for l, e := C.NextSet(0); e; l, e = C.NextSet(l + 1) {
				v := uint(0)      // v s.t. |F_uv| is minimum
				c_min := max_size // Minimum size of F_uv
				count := 0        // Count of |F_uv| <= 2
				for z, fset := range F_u {
					if fset.Test(l) {
						size := fset.Count()
						if size <= 2 {
							count++
						}
						if size <= c_min {
							c_min = size
							v = z
						}
					}
				}
				found = count <= 1
				// Case (1)
				if found {
					G.Set(u, int(v), int(l))
					delete(F_u, v)
					for _, fset := range F_u {
						fset.SetTo(l, false)
					}
					break
				}
			}
			if found {
				continue
			}
			// Case (2)
			G.free[u].Copy(F)
			F.InPlaceDifference(C)
			//F = G.free[u].Difference(C)
			b, _ := F.NextSet(0)
			w := uint(0)
			best_size := max_size
			for v, fset := range F_u {
				size := fset.Count()
				if size < best_size {
					w = v
					best_size = size
				}
			}
			a, _ := F_u[w].NextSet(0)
			// Switch G[0..u][a,b]
			bc := int(b)
			ac := int(a)
			P2 := get_path_subset(G, int(w), bc, ac, P, u)
			switch_path(G, P2, bc, ac)
			G.Set(u, int(w), bc)
			// Update F_u
			// If P2[-1] in W
			if fset, ok := F_u[uint(P2[len(P2)-1])]; ok {
				fset.SetTo(a, false)
			}
			delete(F_u, w)
		}
	}
}
