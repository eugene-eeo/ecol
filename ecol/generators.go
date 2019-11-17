package main

type VMAlgorithm struct {
	Name     string `json:"name"`
	Attempts int    `json:"attempts"`
}

type VMResult struct {
	Name      string `json:"name"`
	Attempts  int    `json:"attempts"`
	Successes int    `json:"successes"`
}

type VMInput struct {
	Class      int           `json:"class"`
	Algorithms []VMAlgorithm `json:"algorithms"`
	EdgeData   [][]int       `json:"edge_data"`
	EmitGraph  bool          `json:"emit_graph"`
	Metadata   interface{}   `json:"metadata"`
}

type VMOutput struct {
	Results  []VMResult  `json:"results"`
	EdgeData [][]int     `json:"edge_data"`
	Metadata interface{} `json:"metadata"`
}
