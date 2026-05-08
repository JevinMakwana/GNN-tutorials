from typing import Set, Tuple
import numpy as np
import pyvista as pv

def extract_faces(mesh: pv.PolyData) -> np.ndarray:
    faces: np.ndarray = mesh.faces.reshape(-1, 4)[:, 1:]
    return faces


def build_edges(mesh: pv.PolyData) -> Set[Tuple[int, int]]:

    faces = extract_faces(mesh)
    edges: Set[Tuple[int, int]] = set()

    for tri in faces:
        a, b, c = tri
        edges.update([
            tuple(sorted((a, b))),
            tuple(sorted((b, c))),
            tuple(sorted((c, a)))
        ])

    return edges