from typing import Set, Tuple
import numpy as np

def create_adjacency_matrix(num_nodes: int, edges: Set[Tuple[int, int]]) -> np.ndarray:
    # Dense adjacency scales as O(N^2); avoid allocating huge matrices.
    max_dense_nodes: int = 15000
    if num_nodes > max_dense_nodes:
        raise MemoryError(
            f"Dense adjacency disabled for {num_nodes} nodes. "
            f"Limit is {max_dense_nodes}."
        )

    adj_matrix: np.ndarray = np.zeros((num_nodes, num_nodes), dtype=np.uint8)

    for u, v in edges:
        adj_matrix[u, v] = 1
        adj_matrix[v, u] = 1

    return adj_matrix