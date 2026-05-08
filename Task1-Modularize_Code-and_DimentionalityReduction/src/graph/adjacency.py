from typing import Set, Tuple
import numpy as np

def create_adjacency_matrix(num_nodes: int, edges: Set[Tuple[int, int]]) -> np.array:
    adj_matrix: np.ndarray = np.zeros((num_nodes, num_nodes), dtype=int)

    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1

    return adj_matrix