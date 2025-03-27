import numpy as np
from shapely.geometry import Polygon
from scipy.spatial.distance import directed_hausdorff


def calculate_metrics(original_vertices, projected_vertices):
    # Ensure input is NumPy array
    original_vertices = np.array(original_vertices)
    projected_vertices = np.array(projected_vertices)

    # Create polygons
    original_polygon = Polygon(original_vertices)
    projected_polygon = Polygon(projected_vertices)

    # 1. Area Distortion
    original_area = original_polygon.area
    projected_area = projected_polygon.area
    if original_area == 0:
        area_distortion = np.inf
    else:
        area_distortion = (projected_area - original_area) / original_area

    # 2. Edge Length Variation
    original_edges = np.linalg.norm(np.roll(original_vertices, -1, axis=0) - original_vertices, axis=1)
    projected_edges = np.linalg.norm(np.roll(projected_vertices, -1, axis=0) - projected_vertices, axis=1)
    edge_length_variation = np.abs(projected_edges - original_edges) / original_edges

    # 3. Angle Deviation
    def calculate_angles(vertices):
        vectors = np.roll(vertices, -1, axis=0) - vertices
        angles = []
        for i in range(len(vectors)):
            v1 = vectors[i - 1] / np.linalg.norm(vectors[i - 1])
            v2 = vectors[i] / np.linalg.norm(vectors[i])
            angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
            angles.append(np.degrees(angle))
        return np.array(angles)

    original_angles = calculate_angles(original_vertices)
    projected_angles = calculate_angles(projected_vertices)
    angle_deviation = np.abs(projected_angles - original_angles)

    # 4. Aspect Ratio Change
    def calculate_diagonal_ratio(vertices):
        distances = np.linalg.norm(vertices[:, np.newaxis] - vertices, axis=2)
        np.fill_diagonal(distances, 0)
        max_dist = np.max(distances)
        min_dist = np.min(distances[np.nonzero(distances)])
        return max_dist / min_dist

    original_aspect_ratio = calculate_diagonal_ratio(original_vertices)
    projected_aspect_ratio = calculate_diagonal_ratio(projected_vertices)
    aspect_ratio_change = projected_aspect_ratio - original_aspect_ratio

    # 5. Shape Similarity Index (using Hausdorff Distance)
    hausdorff_distance = max(directed_hausdorff(original_vertices, projected_vertices)[0],
                             directed_hausdorff(projected_vertices, original_vertices)[0])

    return {
        "area_distortion": area_distortion,
        "max_edge_length_variation": np.max(edge_length_variation),
        "max_angle_deviation": np.max(angle_deviation),
        "aspect_ratio_change": aspect_ratio_change,
        "hausdorff_distance": hausdorff_distance
    }
