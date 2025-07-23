import numpy as np


def complete_cone_surface_apex_neg_z(
   radius,
   cone_angle_deg,
   height=None,
   pos_height_lim=0,
   z_base_offset=0,
   resolution=100
   ):
    # convert angles to radians
    cone_angle_rad = np.deg2rad(cone_angle_deg)
    angle_revolution_rad = np.deg2rad(360)

    # compute height and height_cutoff if not provided
    if height is None:
        height = radius / np.tan(cone_angle_rad)
    # Parametric equations for the cone
    theta = np.linspace(0, angle_revolution_rad, resolution)  # Angle around the cone
    z = np.linspace(-height + z_base_offset, pos_height_lim, resolution)  # Height of the cone
    theta, z = np.meshgrid(theta, z)  # Create a meshgrid
    r = (1 + ((z-z_base_offset) / height)) * radius  # Radius of the cone at height z
    x = r * np.cos(theta)  # x-coordinate
    y = r * np.sin(theta)  # y-coordinate

    return x, y, z


def cone_surface_apex_neg_z(
   radius,
   cone_angle_deg,
   angle_revolution_deg,
   angle_offset_deg,
   height=None,
   height_cutoff=None,
   z_base_offset=0,
   resolution=100
   ):
    # convert angles to radians
    cone_angle_rad = np.deg2rad(cone_angle_deg)
    angle_revolution_rad = np.deg2rad(angle_revolution_deg)
    angle_offset_rad = np.deg2rad(angle_offset_deg)

    # compute height and height_cutoff if not provided
    if height is None:
        height = radius / np.tan(cone_angle_rad)
    if height_cutoff is None:
        height_cutoff = height

    # Parametric equations for the cone
    theta = np.linspace(angle_offset_rad, angle_revolution_rad + angle_offset_rad, resolution)  # Angle around the cone
    z = np.linspace(-height_cutoff + z_base_offset, z_base_offset, resolution)  # Height of the cone
    theta, z = np.meshgrid(theta, z)  # Create a meshgrid
    r = (1 + ((z-z_base_offset) / height)) * radius  # Radius of the cone at height z
    x = r * np.cos(theta)  # x-coordinate
    y = r * np.sin(theta)  # y-coordinate

    return x, y, z


def cone_surface_apex_neg_z_w_blckd_ngl(
    radius,
    cone_angle_deg,
    angle_revolution_deg,
    angle_offset_deg,
    height=None,
    height_cutoff=None,
    z_base_offset=0,
    resolution=100,
    blocked_angle_deg=0,
    outer_blocked_angle_deg=0
):
    # Convert angles to radians
    cone_angle_rad = np.deg2rad(cone_angle_deg)
    angle_revolution_rad = np.deg2rad(angle_revolution_deg)
    angle_offset_rad = np.deg2rad(angle_offset_deg)
    blocked_angle_rad = np.deg2rad(blocked_angle_deg)
    outer_blocked_angle_rad = np.deg2rad(outer_blocked_angle_deg)

    # Compute height and height_cutoff if not provided
    if height is None:
        height = radius / np.tan(cone_angle_rad)
    if height_cutoff is None:
        height_cutoff = height

    # Parametric equations for the cone
    theta = np.linspace(angle_offset_rad, angle_revolution_rad + angle_offset_rad, resolution)  # Angle around the cone
    z = np.linspace(-height_cutoff + z_base_offset, z_base_offset, resolution)  # Height of the cone
    theta, z = np.meshgrid(theta, z)  # Create a meshgrid

    # Compute radius at each z
    r = (1 + ((z - z_base_offset) / height)) * radius  # Radius of the cone at height z

    # Compute interpolated blocked angle at each z
    blocked_angle_at_z = blocked_angle_rad + ((z - (-height_cutoff + z_base_offset)) / height_cutoff) * (outer_blocked_angle_rad - blocked_angle_rad)

    # Mask points within the blocked angle
    mask = (np.abs(theta - angle_offset_rad - np.pi) > blocked_angle_at_z) & (np.abs(theta - angle_offset_rad - np.pi) < (2 * np.pi - blocked_angle_at_z))  # Keep only unblocked angles

    # Apply mask using np.where to keep the 2D structure
    x = np.where(mask, r * np.cos(theta), np.nan)
    y = np.where(mask, r * np.sin(theta), np.nan)
    z = np.where(mask, z, np.nan)  # Set blocked points to NaN

    # # Optionally, remove NaN values if needed
    # x = x[~np.isnan(x)]
    # y = y[~np.isnan(y)]
    # z = z[~np.isnan(z)]
    return x, y, z


def plane_surface_orthogonal_center(
    screen_width,
    screen_height,
    center_z_offset,
    center_distance,
    center_azimuth_deg,
    resolution=100,
):
    # Convert angle to radians
    azimuth_rad = np.radians(center_azimuth_deg)

    # Compute the center point of the screen in 3D
    cx = center_distance * np.cos(azimuth_rad)
    cy = center_distance * np.sin(azimuth_rad)
    cz = center_z_offset
    center = np.array([cx, cy, cz])

    # The normal vector from the origin to the screen center
    normal = center / np.linalg.norm(center)

    # Find two orthogonal vectors (u and v) on the screen plane
    # Choose an arbitrary up direction (z-axis), make sure it's not colinear
    up = np.array([0, 0, 1])
    if np.allclose(np.cross(normal, up), 0):
        up = np.array([0, 1, 0])  # fallback if normal is along z-axis

    # First basis vector on the screen plane
    u = np.cross(normal, up)
    u = u / np.linalg.norm(u)

    # Second basis vector orthogonal to both normal and u
    v = np.cross(normal, u)

    # Generate grid in 2D then map to 3D using u and v
    x = np.linspace(-screen_width / 2, screen_width / 2, resolution)
    y = np.linspace(-screen_height / 2, screen_height / 2, resolution)
    xv, yv = np.meshgrid(x, y)

    # Calculate 3D positions: center + x * u + y * v
    surface = center[:, None, None] + xv[None, :, :] * u[:, None, None] + yv[None, :, :] * v[:, None, None]

    return surface  # shape: (3, resolution, resolution)


def plane_surface_center_tilt(
    screen_width,
    screen_height,
    center_z_offset,
    center_distance,
    center_azimuth_deg,
    tilt_deg=0.0,
    resolution=100,
):
    # Convert angles to radians
    azimuth_rad = np.radians(center_azimuth_deg)
    tilt_rad = np.radians(tilt_deg)

    # Define center position in space
    cx = center_distance * np.cos(azimuth_rad)
    cy = center_distance * np.sin(azimuth_rad)
    cz = center_z_offset
    center = np.array([cx, cy, cz])

    # Forward vector: screen facing along azimuth direction
    forward = np.array([np.cos(azimuth_rad), np.sin(azimuth_rad), 0.0])

    # Right vector: perpendicular to forward, points horizontally right
    right = np.array([-np.sin(azimuth_rad), np.cos(azimuth_rad), 0.0])

    # Up vector: default screen up is vertical
    up = np.array([0.0, 0.0, 1.0])

    # Rotate the forward and up vectors around the right vector by tilt
    def rotate_vector(vec, axis, angle_rad):
        axis = axis / np.linalg.norm(axis)
        return (
            vec * np.cos(angle_rad) +
            np.cross(axis, vec) * np.sin(angle_rad) +
            axis * np.dot(axis, vec) * (1 - np.cos(angle_rad))
        )

    forward_rot = rotate_vector(forward, right, tilt_rad)
    up_rot = rotate_vector(up, right, tilt_rad)

    # Generate the grid on the screen surface
    x = np.linspace(-screen_width / 2, screen_width / 2, resolution)
    y = np.linspace(-screen_height / 2, screen_height / 2, resolution)
    xv, yv = np.meshgrid(x, y)

    # Calculate surface points in 3D
    surface = center[:, None, None] + xv[None, :, :] * right[:, None, None] + yv[None, :, :] * up_rot[:, None, None]

    return surface  # shape: (3, resolution, resolution)