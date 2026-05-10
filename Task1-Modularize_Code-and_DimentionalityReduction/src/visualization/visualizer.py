from typing import Optional
import pyvista as pv
import numpy as np
import torch
import plotly.graph_objects as go

from torch_geometric.data import Data

# def convert_edge_index_to_lines( edge_index: torch.Tensor ) -> np.ndarray:
#     lines: list[int] = []
#     edge_index_np: np.ndarray = edge_index.numpy()
#     num_edges: int = edge_index_np.shape[1]

#     for i in range(num_edges):
#         u: int = edge_index_np[0][i]
#         v: int = edge_index_np[1][i]
#         lines.extend([2, u, v])

#     return np.array(lines)


def visualize_graph( mesh: pv.PolyData, pyg_data: Optional[Data] = None ) -> None:
    # Create Plotly figure
    fig = go.Figure()

    # Add mesh points as scatter plot
    fig.add_trace(go.Scatter3d(
        x=mesh.points[:, 0],
        y=mesh.points[:, 1],
        z=mesh.points[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color='green',
            opacity=0.6
        ),
        name='Original Mesh Points',
        hovertext=[f"Point {i}" for i in range(len(mesh.points))],
        hoverinfo='text'
    ))
    
    if pyg_data:
        points: np.ndarray = pyg_data.x[:, :3].numpy()
        edge_index: np.ndarray = pyg_data.edge_index.numpy()

        # Add graph edges as lines
        edge_x = []
        edge_y = []
        edge_z = []

        for i in range(edge_index.shape[1]):
            u, v = edge_index[0, i], edge_index[1, i]
            edge_x.extend([points[u, 0], points[v, 0], None])
            edge_y.extend([points[u, 1], points[v, 1], None])
            edge_z.extend([points[u, 2], points[v, 2], None])

        fig.add_trace(go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='red', width=1),
            name='Graph Edges',
            hoverinfo='skip'
        ))

        # Add graph nodes
        fig.add_trace(go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode='markers',
            marker=dict(
                size=3,
                color='black',
                opacity=0.8
            ),
            name='Graph Nodes',
            hovertext=[f"Node {i}" for i in range(len(points))],
            hoverinfo='text'
        ))

    fig.update_layout(
        title='CAD Graph Visualization',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        hovermode='closest',
        width=1200,
        height=800
    )

    html_path: str = "visualization_interactive.html"
    fig.write_html(html_path)
    print(f"Interactive visualization saved to: {html_path}")
    print(f"Open this file in a web browser to interact with the 3D visualization")