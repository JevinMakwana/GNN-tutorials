import torch
import pyvista as pv
import numpy as np
from torch_geometric.data import Data
from pathlib import Path
# from typing import Set, Tuple


from config import (
    INPUT_STL_PATH,
    OUTPUT_VTM_PATH,
    OUTPUT_PYG_PATH,
    MODEL_NAME,
)
from src.mesh.loader import load_mesh
from src.mesh.surface import extract_surface
from src.mesh.features import extract_surface_features

# from src.graph.graph_builder import build_edges
from src.graph.graph_builder import build_edge_indeces

# from src.graph.adjacency import create_adjacency_matrix

from src.graph.pyg_converter import create_pyg_data
from src.visualization.visualizer import visualize_graph
from src.export.vtm_exporter import save_vtm


def main() -> None:
    try:
        pv.set_jupyter_backend('html')
    except ImportError:
        pass

    
    print("\nLoading mesh...")
    mesh: pv.PolyData = load_mesh(
        f"{INPUT_STL_PATH}/{MODEL_NAME}.stl"
    )
    print("Number of points in given object:", mesh.n_points)
    print("Number of cells in given object:", mesh.n_cells)    
    # mesh.plot()


    print("\nExtracting surface...")
    surface_mesh: pv.PolyData = extract_surface(
        mesh
    )


    print("\nExtracting surface features...")
    node_features: np.ndarray
    normals: np.ndarray
    node_features, normals = extract_surface_features(
        surface_mesh
    )


    print("\nBuilding graph edges...")
    # edges: Set[Tuple[int, int]] = build_edges(
    #     surface_mesh
    # )
    edge_index: torch.Tensor = build_edge_indeces(mesh)

    # NO NEED TO CREATE ADJACENCY MATRIX AS ARE ARE USING 
    # print("\nCreating adjacency matrix...")
    # adj_matrix: np.ndarray = create_adjacency_matrix(
    #     surface_mesh.n_points,
    #     edges
    # )
    # print( "Adjacency matrix shape:", adj_matrix.shape )



    print("\nCreating PyG graph...")
    pyg_data: Data = create_pyg_data(
        node_features,
        edge_index
        # edges
    )
    print("\nPyG Data Object:-", pyg_data)



    print("\nSaving PyG graph(.pt format)...")
    torch.save(
        pyg_data,
        OUTPUT_PYG_PATH
    )

    print(
        f"Saved PyG graph at: "
        f"{OUTPUT_PYG_PATH}"
    )


    print("\nSaving VTM file...")
    save_vtm(
        surface_mesh,
        edge_index,
        OUTPUT_VTM_PATH
    )
    # save_vtm(
    #     surface_mesh,
    #     edges,
    #     f"{OUTPUT_VTM_PATH}/{MODEL_NAME}.vtm"
    # )


    print("\nLaunching visualization...")
    html_output_path = Path(OUTPUT_PYG_PATH).with_name(
        f"{MODEL_NAME}_visualization_interactive.html"
    )
    visualize_graph(
        surface_mesh,
        pyg_data,
        html_output_path
    )


if __name__ == "__main__":
    main()