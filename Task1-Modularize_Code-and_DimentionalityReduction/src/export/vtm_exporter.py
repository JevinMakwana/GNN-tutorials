from typing import Set, Tuple
import pyvista as pv
import numpy as np
import torch


def build_graph_polydata(
    points: np.ndarray,
    edge_index: torch.Tensor
) -> pv.PolyData:

    lines: list[int] = []

    edge_index_np: np.ndarray = edge_index.detach().cpu().numpy()
    for idx in range(len(edge_index)):
        lines.extend([2, int(edge_index_np[0,idx]), int(edge_index_np[1,idx])])
    
    lines_array: np.ndarray = np.array(lines)

    graph: pv.PolyData = pv.PolyData()
    graph.points = points
    graph.lines = lines_array

    return graph

# def build_graph_polydata(
#     points: np.ndarray,
#     edge_index: torch.Tensor
# ) -> pv.PolyData:

#     lines: list[int] = []

#     edge_index_np: np.ndarray = edge_index.detach().cpu().numpy()

#     for idx in range(edge_index_np.shape[1]):
#         u: int = int(edge_index_np[0, idx])
#         v: int = int(edge_index_np[1, idx])
#         lines.extend([2, u, v])
    
#     lines_array: np.ndarray = np.array(lines)

#     graph: pv.PolyData = pv.PolyData()
#     graph.points = points
#     graph.lines = lines_array

#     return graph

# def build_graph_polydata(
#     points: np.ndarray,
#     edges: Set[Tuple[int, int]]
# ) -> pv.PolyData:

#     lines: list[int] = []

#     for u, v in edges:
#         lines.extend([2, u, v])

#     lines_array: np.ndarray = np.array(lines)

#     graph: pv.PolyData = pv.PolyData()
#     graph.points = points
#     graph.lines = lines_array

#     return graph


def save_vtm(
    mesh: pv.PolyData,
    edge_index: torch.Tensor,
    output_path: str
) -> None:

    graph: pv.PolyData = build_graph_polydata(
        mesh.points,
        edge_index
    )

    multi: pv.MultiBlock = pv.MultiBlock()

    multi['mesh'] = mesh
    multi['graph'] = graph
    multi.save(output_path)

    print(f"Saved VTM file at: {output_path}")
    
# def save_vtm(
#     mesh: pv.PolyData,
#     edges: Set[Tuple[int, int]],
#     output_path: str
# ) -> None:

#     graph: pv.PolyData = build_graph_polydata(
#         mesh.points,
#         edges
#     )

#     multi: pv.MultiBlock = pv.MultiBlock()

#     multi['mesh'] = mesh
#     multi['graph'] = graph
#     multi.save(output_path)

#     print(f"Saved VTM file at: {output_path}")