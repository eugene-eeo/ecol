import sys
import json


if __name__ == '__main__':
    for line in sys.stdin:
        u = json.loads(line)
        edge_data = u["edge_data"]
        print(f"{len(edge_data)}|{line.strip()}")
