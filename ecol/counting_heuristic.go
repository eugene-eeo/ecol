package main

import "github.com/willf/bitset"

type FreesetInfo struct {
	fset *bitset.BitSet
	size uint
}

func counting_heuristic_colour(G *ColouringGraph) {
	delta := uint(max_degree(G))
	colours := bitset.New(delta + 2).Complement()
	colours.SetTo(0, false)
	G.AddColours(colours)
	max_size := delta + 2

	P := allocate_path_array(G)
	C := bitset.New(uint(G.g.n))
	F := bitset.New(uint(G.g.n))

	F_u := make(map[int]*FreesetInfo, G.g.n)
	// Use this to populate F_u to avoid reallocs
	fset_cache := make([]*FreesetInfo, G.g.n)
	for i := range fset_cache {
		fset_cache[i] = &FreesetInfo{bitset.New(delta + 2), 0}
	}

	for u := 0; u < G.g.n; u++ {
	RESTART:
		// u := current node to colour
		// Compute F_u[x] = F(ux) = F(u) & F(x)
		// Everything up to u is in V
		N := 0
		f_u := G.free[u]
		r := G.g.edge_data[u]
		for v := 0; v < u; v++ {
			if r[v] == 0 {
				fi := fset_cache[v]
				f_u.Copy(fi.fset)
				fi.fset.InPlaceIntersection(G.free[v])
				fi.size = fi.fset.Count()
				F_u[v] = fi
				N++
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
						fi.fset.SetTo(l, false)
						fi.size = fi.fset.Count()
					}
					continue OUTER
				}
			}
			// Case (2)
			G.free[u].Copy(F)
			F.InPlaceDifference(C)
			b, e := F.NextSet(0)
			if !e {
				G.AddColour(delta + 1)
				goto RESTART
			}
			w := 0
			best_size := max_size
			for v, fi := range F_u {
				if fi.size <= best_size {
					w = v
					best_size = fi.size
				}
			}
			a, e := F_u[w].fset.NextSet(0)
			if !e {
				G.AddColour(delta + 1)
				goto RESTART
			}
			// Switch G[0..u][a,b]
			P2 := get_path_subset(G, w, int(b), int(a), P, u)
			switch_path(G, P2, int(b), int(a))
			G.Set(u, w, int(b))
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
