from typing import Tuple
import numpy as np
import pyvista as pv

def compute_normals(mesh: pv.PolyData) -> np.ndarray:
    mesh_with_normals = mesh.compute_normals(
        cell_normals=False,
        point_normals=True
    )
    normals: np.ndarray = mesh_with_normals.point_data['Normals']

    return normals


def extract_surface_features(mesh: pv.PolyData) -> Tuple[np.ndarray, np.ndarray]:
    points: np.ndarray = mesh.points
    normals: np.ndarray = compute_normals(mesh)
    
    # node_feature = x_coord, y_coord, z_coord, x_normal, y_normal, z_normal
    node_features: np.ndarray = np.hstack([points, normals])

    return node_features, normals