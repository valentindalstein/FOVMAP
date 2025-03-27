import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

CPS_COLOR = "green"
HGPS_COLOR = "blue"
REM_COLOR = "red"
SEL_COLOR = "y"
CAN_COLOR = "purple"
CUR_CP_COLOR = "k"
EDGE_COLOR = "gray"
SMALL_SIZE = 6
MEDIUM_SIZE = 10
BIG_SIZE = 20


def on_key(event):
    # Check if the key pressed is Enter (you can customize it to other keys if needed)
    if event.key == 'enter':
        plt.close()  # Close the plot when Enter is pressed


def set_view_from_vector(ax, vector):
    elevation, azimuth = ele_azim_from_vector_for_plot(vector)
    # Set the view
    ax.view_init(elev=elevation, azim=azimuth)


def ele_azim_from_vector_for_plot(vector):
    # Normalize the vector
    vector = -np.array(vector)  # to face in the same direction otherwise its opposite
    vector = vector / np.linalg.norm(vector)
    # Compute angles
    azimuth = np.degrees(np.arctan2(vector[1], vector[0]))  # Angle in XY-plane
    elevation = np.degrees(np.arcsin(vector[2]))  # Angle from XY-plane
    return elevation, azimuth


def plot_candidates(
   current,
   candidates,
   cps,
   hgps,
   remaining_points,
   edges
   ):
    # make sure there are no overlapping points
    # check remaining points
    remaining_points_copy = remaining_points.copy()
    for edge in edges:
        if edge in remaining_points_copy:
            remaining_points_copy.remove(edge)
    if current in remaining_points_copy:
        remaining_points_copy.remove(current)
    for candidate in candidates:
        if candidate in remaining_points_copy:
            remaining_points_copy.remove(candidate)
    for cp in cps:
        if cp in remaining_points_copy:
            remaining_points_copy.remove(cp)
    for hgp in hgps:
        if hgp in remaining_points_copy:
            remaining_points_copy.remove(hgp)
    # check hex grid points
    hgps_copy = hgps.copy()
    for candidate in candidates:
        if candidate in hgps:
            hgps_copy.remove(candidate)
    # check cps and current
    cps_copy = cps.copy()
    if current in cps_copy:
        cps_copy.remove(current)
    # create the figure
    fig = plt.gcf()
    canvas = fig.canvas

    # get the Qt window object and set it to fullscreen
    canvas.manager.window.showFullScreen()
    fig.canvas.mpl_connect('key_press_event', on_key)  # close with enter

    # create the 3D plot set the axis properly
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_aspect('equal')

    # plot the points if list not empty
    if edges:
        ax.scatter(*zip(*edges), color=EDGE_COLOR, s=SMALL_SIZE, alpha=1)
    if remaining_points_copy:
        ax.scatter(*zip(*remaining_points_copy), color=REM_COLOR, s=SMALL_SIZE, alpha=1)
    if cps_copy:
        ax.scatter(*zip(*cps_copy), color=CPS_COLOR, s=MEDIUM_SIZE, alpha=1)
    if hgps_copy:
        ax.scatter(*zip(*hgps_copy), color=HGPS_COLOR, s=MEDIUM_SIZE, alpha=1)
    if candidates:
        ax.scatter(*zip(*candidates), color=CAN_COLOR, s=BIG_SIZE, alpha=1)
    ax.scatter(*current, color=CUR_CP_COLOR, s=BIG_SIZE, alpha=1)
    # Adjust view to face the given vector
    set_view_from_vector(ax, current)
    # block until enter pressed
    plt.show(block=True)


def plot_candidates_and_selected(
   current,
   selected,
   candidates,
   cps,
   hgps,
   remaining_points,
   edges
   ):
    # make sure there are no overlapping points
    # check remaining points
    remaining_points_copy = remaining_points.copy()
    for edge in edges:
        if edge in remaining_points_copy:
            remaining_points_copy.remove(edge)
    if selected in remaining_points_copy:
        remaining_points_copy.remove(selected)
    if current in remaining_points_copy:
        remaining_points_copy.remove(current)
    for candidate in candidates:
        if candidate in remaining_points_copy:
            remaining_points_copy.remove(candidate)
    for cp in cps:
        if cp in remaining_points_copy:
            remaining_points_copy.remove(cp)
    for hgp in hgps:
        if hgp in remaining_points_copy:
            remaining_points_copy.remove(hgp)
    # check hex grid points
    hgps_copy = hgps.copy()
    for candidate in candidates:
        if candidate in hgps_copy:
            hgps_copy.remove(candidate)
    if selected in hgps_copy:
        hgps_copy.remove(selected)
    # check candidates
    candidates_copy = candidates.copy()
    if selected in candidates_copy:
        candidates_copy.remove(selected)
    # check cps and current
    cps_copy = cps.copy()
    if current in cps_copy:
        cps_copy.remove(current)
    fig = plt.gcf()
    canvas = fig.canvas

    # Get the Qt window object and set it to fullscreen
    canvas.manager.window.showFullScreen()

    # get the Qt window object and set it to fullscreen
    fig.canvas.mpl_connect('key_press_event', on_key)

    # create the 3D plot set the axis properly
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_aspect('equal')

    # plot the points if list not empty
    if edges:
        ax.scatter(*zip(*edges), color=EDGE_COLOR, s=SMALL_SIZE, alpha=1)
    if remaining_points_copy:
        ax.scatter(*zip(*remaining_points_copy), color=REM_COLOR, s=SMALL_SIZE, alpha=1)
    if cps_copy:
        ax.scatter(*zip(*cps_copy), color=CPS_COLOR, s=MEDIUM_SIZE, alpha=1)
    if hgps_copy:
        ax.scatter(*zip(*hgps_copy), color=HGPS_COLOR, s=MEDIUM_SIZE, alpha=1)
    if candidates_copy:
        ax.scatter(*zip(*candidates_copy), color=CAN_COLOR, s=BIG_SIZE, alpha=1)
    ax.scatter(*current, c=CUR_CP_COLOR, s=BIG_SIZE, alpha=1)
    ax.scatter(*selected, c=SEL_COLOR, s=BIG_SIZE, alpha=1)
    # Adjust view to face the given vector
    set_view_from_vector(ax, current)
    plt.show(block=True)


# Function to visualize the polyhedron
def visualize_polyhedron(vertices, faces):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a Poly3DCollection from the faces
    poly3d = [[vertices[vertex_idx] for vertex_idx in face] for face in faces]
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='gainsboro', linewidths=1, edgecolors='k', alpha=0.75))
    ax.set_box_aspect([1, 1, 1])
    # Set the aspect ratio and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    plt.show()


def visualize_lens_dir(vertices, viewing_dir):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a Poly3DCollection from the faces
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])
    ax.set_box_aspect([1, 1, 1])
    # Set the aspect ratio and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    set_view_from_vector(ax, viewing_dir)
    plt.show()


def plot_cone(x, y, z, fig=None, ax=None):
    if fig is None or ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='gray', alpha=0.25)
    max_dist = max(x.max(), y.max(), z.max())
    # ignore nan values
    max_dist = max(np.nanmax(x), np.nanmax(y), np.nanmax(z))
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-max_dist, max_dist)
    ax.set_zlim(-max_dist, max_dist)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_box_aspect([1, 1, 1])
    # Set title
    # ax.set_title('Plotting cone')
    # Set the view angle
    ax.view_init(elev=30, azim=180, roll=0)
    return fig, ax


def plot_cone_vert(cone_x, cone_y, cone_z, vertices, fig=None, ax=None):
    if fig is None or ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(cone_x, cone_y, cone_z, color='gray', alpha=0.25, label='Cone')
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='r', s=3, label='Right Eye')
    ax.scatter(vertices[:, 0], -vertices[:, 1], vertices[:, 2], color='y', s=3, label='Left Eye')
    ax.set_box_aspect([1, 1, 1])
    # ignore nan values
    max_dist = max(np.nanmax(cone_x), np.nanmax(cone_y), np.nanmax(cone_z))
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-max_dist, max_dist)
    ax.set_zlim(-max_dist, max_dist)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(["Cone", "Right Eye", "Left Eye"])
    ax.set_title('Intersection of Lens Directions and Cone')
    # Set the view angle
    ax.view_init(elev=30, azim=180, roll=0)
    return fig, ax
