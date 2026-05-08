import pyvista as pv
import numpy as np
import torch

from torch_geometric.data import Data

def convert_edge_index_to_lines( edge_index: torch.Tensor ) -> np.ndarray:
    lines: list[int] = []
    edge_index_np: np.ndarray = edge_index.numpy()
    num_edges: int = edge_index_np.shape[1]

    for i in range(num_edges):
        u: int = int(edge_index_np[0, i])
        v: int = int(edge_index_np[1, i])
        lines.extend([2, u, v])

    return np.array(lines)


def visualize_graph( mesh: pv.PolyData, pyg_data: Data ) -> None:
    points: np.ndarray = pyg_data.x[:, :3].numpy()
    lines: np.ndarray = convert_edge_index_to_lines( pyg_data.edge_index )

    graph: pv.PolyData = pv.PolyData()
    graph.points = points
    graph.lines = lines

    plotter: pv.Plotter = pv.Plotter( notebook=True )

    # original mesh
    plotter.add_mesh(
        mesh,
        color='lightblue',
        opacity=0.25
    )

    # graph edges
    plotter.add_mesh(
        graph,
        color='red',
        line_width=1
    )

    # graph nodes
    plotter.add_points(
        points,
        color='black',
        point_size=5,
        render_points_as_spheres=True
    )

    plotter.add_axes()

    plotter.add_text(
        "Light Blue : Original Mesh\n"
        "Red : Graph Edges\n"
        "Black : Graph Nodes",
        position='upper_left',
        font_size=10
    )

    plotter.show(jupyter_backend='html')