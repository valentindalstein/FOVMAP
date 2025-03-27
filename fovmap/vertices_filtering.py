import numpy as np


def filter_vert_z_bound(vertices, z_bounds):
    """
    Filter vertices based on z-boundaries.
    Parameters
    ----------
    vertices : list of list
        List of vertices.
    z_bounds : list
        List of z-boundaries.
    Returns
    -------
    list of list
        Filtered vertices.
    """
    filtered_vertices = []
    for vert in vertices:
        if vert[2] is not None:
            if z_bounds[0] <= vert[2] <= z_bounds[1]:
                filtered_vertices.append(vert)
    return np.array(filtered_vertices)


def filter_vert_z_bound_w_none(vertices, z_bounds):
    """
    Filter vertices based on z-boundaries.
    Parameters
    ----------
    vertices : list of list
        List of vertices.
    z_bounds : list
        List of z-boundaries.
    Returns
    -------
    list of list
        Filtered vertices.
    """
    filtered_vertices = []
    for vert in vertices:
        if vert[2] is None:
            filtered_vertices.append(vert)
        elif z_bounds[0] <= vert[2] <= z_bounds[1]:
            filtered_vertices.append(vert)
        else:
            filtered_vertices.append([None, None, None])
    return np.array(filtered_vertices)
