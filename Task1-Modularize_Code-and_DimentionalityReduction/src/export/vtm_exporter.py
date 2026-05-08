from typing import Set, Tuple
import pyvista as pv
import numpy as np


def build_graph_polydata(
    points: np.ndarray,
    edges: Set[Tuple[int, int]]
) -> pv.PolyData:

    lines: list[int] = []

    for u, v in edges:
        lines.extend([2, u, v])

    lines_array: np.ndarray = np.array(lines)

    graph: pv.PolyData = pv.PolyData()
    graph.points = points
    graph.lines = lines_array

    return graph


def save_vtm(
    mesh: pv.PolyData,
    edges: Set[Tuple[int, int]],
    output_path: str
) -> None:

    graph: pv.PolyData = build_graph_polydata(
        mesh.points,
        edges
    )

    multi: pv.MultiBlock = pv.MultiBlock()

    multi['mesh'] = mesh
    multi['graph'] = graph
    multi.save(output_path)

    print(f"Saved VTM file at: {output_path}")