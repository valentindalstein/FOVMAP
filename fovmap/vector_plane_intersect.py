import numpy as np


def z_oriented_screen_plane_equation(
    center_z_offset,
    center_distance,
    center_azimuth_deg,
    tilt_deg=0.0,
):
    """
    This function computes the plane equation of a screen in 3D space,
    given its center position, azimuth angle, and tilt angle. The plane
    is first computed using its center point. First using the azimuth
    angle and center distance. Two vectors are created, one normal to the plane,
    basically the origin to the center point. And second a vector of the plane,
    the tangent of the center point with a circle that has 0 has a center and 
    center_distance as radius. Note that both vectors have no z components, they are
    both comprised in the plane defined by the axis x and y.
    It's only after computation of these angles that the final plane can be created.
    The center is moved along z using the offset. And the normal vector tilted 
    along the tangent vector.
    With 0 tilt angle, the plane is always colinear with the z-axis. With a tilt angle
    it is not colinear anymore with z.

    Args:
        center_z_offset (float): the offset of the center point along the z-axis.
        center_distance (float): the distance from the center of the plane to the origin.
        center_azimuth_deg (float): the azimuth angle of the center point in degrees.
        tilt_deg (float, optional): the tilt of the plane. Defaults to 0.0.

    Returns:
        floats: the parameters of the plane equation in the form ax + by + cz + d = 0.
    """
    # Convert angles to radians
    azimuth_rad = np.radians(center_azimuth_deg)
    tilt_rad = np.radians(tilt_deg)

    # Center point in space
    cx = center_distance * np.cos(azimuth_rad)
    cy = center_distance * np.sin(azimuth_rad)
    cz = center_z_offset
    center = np.array([cx, cy, cz])

    # Forward vector = screen normal (facing outward from center along azimuth)
    forward = np.array([np.cos(azimuth_rad), np.sin(azimuth_rad), 0.0])

    # Right vector = perpendicular to forward (in plane of screen)
    right = np.array([-np.sin(azimuth_rad), np.cos(azimuth_rad), 0.0])

    # Up vector = vertical
    up = np.array([0.0, 0.0, 1.0])

    # Tilt the forward vector around the right vector
    def rotate_vector(vec, axis, angle_rad):
        axis = axis / np.linalg.norm(axis)
        return (
            vec * np.cos(angle_rad) +
            np.cross(axis, vec) * np.sin(angle_rad) +
            axis * np.dot(axis, vec) * (1 - np.cos(angle_rad))
        )

    # Rotated screen normal vector
    normal = rotate_vector(forward, right, tilt_rad)
    normal /= np.linalg.norm(normal)

    # Plane equation coefficients: a, b, c, d
    a, b, c = normal
    d = -np.dot(normal, center)

    return a, b, c, d  # so that: a*x + b*y + c*z + d = 0


def intersect_ray_with_plane(ray_direction, plane_coeffs, ray_origin=(0,0,0)):
    """
    Intersects a ray with a plane defined by its coefficients.

    Args:
        ray_origin (np.ndarray): The origin of the ray (3D point).
        ray_direction (np.ndarray): The direction of the ray (3D vector).
        plane_coeffs (tuple): Coefficients of the plane equation (a, b, c, d).

    Returns:
        np.ndarray: The intersection point if it exists, otherwise None.
    """
    a, b, c, d = plane_coeffs
    denom = a * ray_direction[0] + b * ray_direction[1] + c * ray_direction[2]

    if np.abs(denom) < 1e-6:  # Check if the ray is parallel to the plane
        return None

    t = -(a * ray_origin[0] + b * ray_origin[1] + c * ray_origin[2] + d) / denom
    if t < 0:  # Check if the intersection is behind the ray origin
        return None

    intersection_point = ray_origin + t * ray_direction
    return intersection_point


def intersect_rays_with_plane(ray_directions, plane_coeffs, ray_origins=None):
    """
    Intersects multiple rays with a plane defined by its coefficients.

    Args:
        ray_origins (np.ndarray): Origins of the rays (N x 3 array).
        ray_directions (np.ndarray): Directions of the rays (N x 3 array).
        plane_coeffs (tuple): Coefficients of the plane equation (a, b, c, d).

    Returns:
        np.ndarray: Intersection points (N x 3 array) or None for non-intersections.
    """
    intersections = []
    if ray_origins is None:
        ray_origins = np.zeros_like(ray_directions)

    for origin, direction in zip(ray_origins, ray_directions):
        intersection = intersect_ray_with_plane(origin, direction, plane_coeffs)
        intersections.append(intersection)

    return np.array(intersections)