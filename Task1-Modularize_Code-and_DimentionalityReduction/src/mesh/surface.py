import pyvista as pv

def extract_surface(mesh: pv.PolyData) -> pv.PolyData:
    surface_mesh: pv.PolyData = mesh.extract_surface(
        # algorithm='dataset_surface'
    )
    print("====================surface_mesh[]============",surface_mesh)

    return surface_mesh