import numpy as np


def triangle_area_3d(A, B, C):
    """
    Compute the area of a triangle in 3D space given its vertices A, B, and C.

    Parameters:
        A, B, C: Tuples or lists of (x, y, z) coordinates.

    Returns:
        Area of the triangle.
    """
    AB = np.array(B) - np.array(A)
    AC = np.array(C) - np.array(A)
    
    # Compute cross product
    cross_product = np.cross(AB, AC)
    
    # Triangle area is half the magnitude of the cross product
    area = 0.5 * np.linalg.norm(cross_product)
    
    return area


def order_hexagon_vertices(points):
    """
    Orders the 3D hexagon vertices in a consistent circular order.

    Args:
        points (ndarray): (6, 3) array of 3D coordinates.

    Returns:
        ordered_points (ndarray): (6, 3) array of sorted hexagon vertices.
    """
    if isinstance(points, list):
        points = np.array(points)
    # Compute centroid
    centroid = np.mean(points, axis=0)

    # Find normal of best-fit plane using SVD
    _, _, vh = np.linalg.svd(points - centroid)
    normal = vh[-1]  # Plane normal (smallest singular value)

    # Choose a reference axis on the plane
    ref_vector = points[0] - centroid
    ref_vector /= np.linalg.norm(ref_vector)  # Normalize

    # Compute angles between ref_vector and all other points
    angles = []
    for p in points:
        v = p - centroid
        v /= np.linalg.norm(v)  # Normalize
        cross_prod = np.cross(ref_vector, v)
        dot_prod = np.dot(ref_vector, v)
        angle = np.arctan2(np.dot(cross_prod, normal), dot_prod)
        angles.append(angle)

    # Sort points by angle
    sorted_indices = np.argsort(angles)
    ordered_points = points[sorted_indices]

    return ordered_points.tolist()


def ordered_hexagon_surface(hexagon_vertices):
    """
    Compute the surface area of an ordered hexagon in 3D space given its vertices.

    Parameters:
        hexagon_vertices: List of tuples or lists of (x, y, z) coordinates of the hexagon vertices.

    Returns:
        Surface area of the hexagon.
    """
    # Compute the area of the six triangles formed by the hexagon vertices
    assert len(hexagon_vertices) == 6, "Hexagon must have exactly 6 vertices"
    ordered_vertices = order_hexagon_vertices(hexagon_vertices)
    A = ordered_vertices[0]
    total_area = 0
    for i in range(4):
        B = ordered_vertices[(i + 1)]
        C = ordered_vertices[(i + 2)]
        total_area += triangle_area_3d(A, B, C)

    return total_area


def project_onto_plane(vector, points):
    vector = np.array(vector, dtype=float)
    points = np.array(points, dtype=float)
    
    # Normalize the vector
    normal = vector / np.linalg.norm(vector)

    # Project points onto the plane orthogonal to the normal that contains (0,0,0)
    projected_points = points - np.outer(points @ normal, normal)

    # Find an orthonormal basis for the plane
    # Pick an arbitrary vector not parallel to the normal
    arbitrary = np.array([1, 0, 0]) if abs(normal[0]) < abs(normal[2]) else np.array([0, 0, 1])
    basis1 = np.cross(normal, arbitrary)
    basis1 /= np.linalg.norm(basis1)  # Normalize
    basis2 = np.cross(normal, basis1)  # Second orthogonal basis vector
    
    # Convert 3D projected points to 2D coordinates
    points_2d = np.column_stack((projected_points @ basis1, projected_points @ basis2))
    
    return points_2d


def polygon_area(points_2d):
    """Compute the area of a polygon given its 2D points using the Shoelace theorem."""
    x, y = points_2d[:, 0], points_2d[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def surface_of_projected_polygon(vector, points):
    points_2d = project_onto_plane(vector, points)
    return polygon_area(points_2d)