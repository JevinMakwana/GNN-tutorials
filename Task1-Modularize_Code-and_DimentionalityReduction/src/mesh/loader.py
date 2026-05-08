import pyvista as pv

def load_mesh(path: str) -> pv.PolyData:
    mesh: pv.PolyData = pv.read(path)
    return mesh