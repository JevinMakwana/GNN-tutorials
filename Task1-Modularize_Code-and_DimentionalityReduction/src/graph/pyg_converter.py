from typing import Set, Tuple
import numpy as np
import torch

from torch_geometric.data import Data


def create_edge_index( edges: Set[Tuple[int, int]] ) -> torch.Tensor:
    edge_index: torch.Tensor = torch.tensor(
        list(edges),
        dtype=torch.long
    ).t().contiguous()

    return edge_index


def create_pyg_data( node_features: np.ndarray, edges: Set[Tuple[int, int]] ) -> Data:
    edge_index = create_edge_index(edges)

    x: torch.Tensor = torch.tensor(
        node_features,
        dtype=torch.float
    )

    data: Data = Data(
        x=x,
        edge_index=edge_index
    )

    return data