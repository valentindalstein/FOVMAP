import json
import numpy as np
import pandas as pd

from fovmap.surface_calc import order_hexagon_vertices


# Function to parse the constants, vertices, and faces from the file
def parse_polyhedron_file(filename):
    constants = {}
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        parsing_constants = False
        parsing_vertices = False
        parsing_faces = False
        for line in lines:
            line = line.strip()
            line = line.replace(" ", "")
            if line.startswith("C0="):
                parsing_constants = True
                parsing_vertices = False
                parsing_faces = False
            elif line.startswith("Vertices:"):
                parsing_constants = False
                parsing_vertices = True
                parsing_faces = False
                continue
            elif line.startswith("Faces:"):
                parsing_constants = False
                parsing_vertices = False
                parsing_faces = True
                continue

            if parsing_constants and "=" in line:
                # Parse constants
                key, value = line.split("=")
                key = key.strip()
                value = float(value.strip())
                constants[key] = value

            if parsing_vertices and line.startswith("V"):
                # Extract vertex coordinates
                vertex_data = line.split("=")[1].strip().strip("()")
                list_vertex = vertex_data.split(",")
                for ind, vert in enumerate(list_vertex):
                    if vert in constants.keys():
                        list_vertex[ind] = float(constants[vert])
                    elif vert[1::] in constants.keys():
                        list_vertex[ind] = -float(constants[vert[1::]])
                    else:
                        list_vertex[ind] = float(vert)
                # Split into individual components and convert to floats
                coords = tuple(map(float, list_vertex))
                vertices.append(coords)

            elif parsing_faces and line.startswith("{"):
                # Extract face indices
                face_data = line.strip("{}").strip().split(",")
                face = list(map(int, face_data))
                faces.append(face)

    return np.array(vertices), faces


def convert_polyhedron_to_json(filename):
    vertices, faces = parse_polyhedron_file(filename)
    polyhedron = {"vertices": vertices.tolist(), "faces": faces}
    # save the polyhedron as a json file
    json_filename = str(filename).replace(".txt", ".json")
    with open(json_filename, 'w') as file:
        json.dump(polyhedron, file, indent=4)


def parse_lens_dir_csv_file(filename):
    vertices = []
    n = 0
    for line in open(filename, 'r'):
        if n != 0:
            line = line.strip()
            line = line.replace(" ", "")
            list_vertex = line.split(",")
            for ind, vert in enumerate(list_vertex):
                list_vertex[ind] = float(vert)
            # Split into individual components and convert to floats
            coords = tuple(map(float, list_vertex))
            vertices.append(coords)
        n += 1
    return np.array(vertices)


def rotation_matrix_x(theta):
    """Rotation matrix around the X-axis"""
    theta = np.radians(theta)
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])


def rotation_matrix_y(theta):
    """Rotation matrix around the Y-axis"""
    theta = np.radians(theta)
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]])


def rotation_matrix_z(theta):
    """Rotation matrix around the Z-axis"""
    theta = np.radians(theta)
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]])


def rotate_vectors(vectors, rx, ry, rz):
    """Rotate vectors by rx, ry, rz degrees around x, y, z axes"""
    R = rotation_matrix_x(rx) @ rotation_matrix_y(ry) @ rotation_matrix_z(rz)
    return np.dot(vectors, R.T)  # Apply rotation


def convert_vertices_to_index(vertices, vertice):
    return vertices.index(vertice)


def convert_faces_to_indices(vertices, hg_dict):
    for key, face_dict in hg_dict.items():
        face = face_dict["surrounding"]
        ordered_face = order_hexagon_vertices(face)
        face_indices = []
        for vertice in ordered_face:
            face_indices.append(convert_vertices_to_index(vertices, vertice))
        hg_dict[key]["face"] = face_indices
    return hg_dict


def load_manual_hex_grid_face_list(vertices, file_path):
    if isinstance(vertices, np.ndarray):
        vertices = vertices.tolist()
    with open(file_path, 'r') as file:
        hg_dict = json.load(file)
    hg_dict_w_faces = convert_faces_to_indices(vertices=vertices, hg_dict=hg_dict)
    face_list = [local_dict["face"] for local_dict in hg_dict_w_faces.values()]
    return face_list


def create_intersect_df(face_list, intersect_dict):
    face_intersect_dict = {}
    for index, face in enumerate(face_list):
        face_intersect_dict[index] = {
            "om_vertices": [intersect_dict[vert_index]["om_dir"] for vert_index in face],
            "om_ints": [intersect_dict[vert_index]["om_int"] for vert_index in face],
            "t_intersects": [intersect_dict[vert_index]["t_intersect"] for vert_index in face]
            }
    return pd.DataFrame.from_dict(face_intersect_dict, orient='index')