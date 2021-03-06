// Parser for the graph6 format: http://users.cecs.anu.edu.au/~bdm/data/formats.txt

package main

func graph6_get_size(data []byte) (cursor int, size int) {
	m := 0 // number of leading 126s
	for i := 0; i < len(data); i++ {
		if data[i] == 126 {
			m++
		} else {
			break
		}
	}
	// 3 cases for m:
	// (0) N(n) = n+63         [1 bytes]
	// (1) N(n) = 126 R(x)     [4 bytes]
	// (2) N(n) = 126 126 R(x) [8 bytes]
	switch m {
	case 0:
		cursor = 1
	case 1:
		cursor = 4
	case 2:
		cursor = 8
	}
	for i := m; i < cursor; i++ {
		size += (1 << (6 * uint(cursor-i-1))) * (int(data[i]) - 63)
	}
	return
}

func graph6_write_graph(data []byte, size int, graph *Graph) {
	k := 0
	// Generate ordering (0,1),(0,2),(1,2),(0,3),(1,3),(2,3),...
	// Might look weird but consider:
	//   (1,0),
	//   (2,0),(2,1),
	//   (3,0),(3,1),(3,2),
	//   ...
	for v := 0; v < size; v++ {
		for u := 0; u < v; u++ {
			b := (data[k/6] - 63) << 2  // relevant byte
			m := byte(1 << uint(7-k%6)) // mask
			if (b & m) != 0 {
				graph.Set(u, v, 0)
			} else {
				graph.Set(u, v, -1)
			}
			k++
		}
	}
}

// func ParseGraph6Bytes(data []byte) *Graph {
// 	cursor, size := get_size(data)
// 	return get_graph(data[cursor:], size)
// }
