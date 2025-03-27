import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import cKDTree


def categorize_face(face):
    length = len(face)
    n = 0
    for vert in face:
        if vert[0] is None:
            n += 1
    if n == length:
        return "no_intersection"
    elif n == 0:
        return "full_intersection"
    else:
        return "partial_intersection"


def plot_hexagonal_surface(vertices, ax):
    if vertices.shape != (6, 3):
        raise ValueError("Each hexagon must have exactly 6 vertices with 3D coordinates.")

    # Create and add hexagonal face
    hexagon = Poly3DCollection([vertices], alpha=0.5, edgecolor='k')
    ax.add_collection3d(hexagon)


def plot_hexagonal_surfaces_from_df(df, col_name, hue_col=None, fig=None, ax=None):
    """
    Plots multiple hexagonal surfaces stored in a DataFrame with optional coloring.

    Parameters:
        df (pd.DataFrame): DataFrame where each row contains a hexagonal face
                           as a list of six 3D points.
                           Each row should have a 'vertices' column with an array (6,3).
        col_name (str): Name of the column containing the vertices.
        hue_col (str, optional): Name of the column to use for coloring the surfaces.
                                 Values should be numeric or mappable to a colormap.
    """
    if fig is None or ax is None:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

    all_points = []

    # Normalize hue values if hue_col is provided
    if hue_col:
        hue_values = df[hue_col].values
        norm = plt.Normalize(vmin=np.min(hue_values), vmax=np.max(hue_values))
        cmap = plt.cm.viridis  # You can choose a different colormap if desired

    for _, row in df.iterrows():
        vertices = np.array(row[col_name])  # Convert to NumPy array if not already

        # Determine face color based on hue_col
        if hue_col:
            color = cmap(norm(row[hue_col]))
        else:
            color = 'cyan'  # Default color if no hue_col is provided

        # Plot the hexagonal surface
        hexagon = Poly3DCollection([vertices], alpha=1, edgecolor='k', facecolor=color)
        ax.add_collection3d(hexagon)

        # Collect points for axis scaling
        all_points.append(vertices)

    # Flatten list and convert to array
    all_points = np.vstack(all_points)

    # Scatter all vertices
    # ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], color='k', s=3, alpha=0.5)

    # Set axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Add a colorbar if hue_col is provided
    if hue_col:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.5, aspect=10)
        cbar.set_label(hue_col)
    return fig, ax


def project_points_on_surface(x, y, z, points):

    # Flatten surface points
    surface_points = np.column_stack([x.ravel(), y.ravel(), z.ravel()])

    # Build KDTree for nearest neighbor search
    tree = cKDTree(surface_points)
    projected_points = np.zeros_like(points)
    for index, point in enumerate(points):
        if point[0] is None:
            projected_points[index] = point
        else:
            # Find closest points on the surface
            distances, indices = tree.query(point)

            # Get the corresponding surface points
            projected_points[index] = surface_points[indices]
    return projected_points
