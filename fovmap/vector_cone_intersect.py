import numpy as np


def vector_cone_intersection(
    radius,
    height,
    vertices
):
    intersection_points = {}
    ommatidia_to_intersection = {}
    P0 = np.array([0, 0, 0])  # Starting point of the vector
    for ind, vert in enumerate(vertices):
        # Define the vector (parametric line)
        # Vector equation: P = P0 + t * direction

        direction = np.array(vert)  # Direction of the vector

        # Find the intersection between the vector and the cone
        # Cone equation: (x^2 + y^2) = (radius * (1 + z / height))^2
        # Substitute the vector equation into the cone equation:
        # (P0[0] + t * direction[0])^2 + (P0[1] + t * direction[1])^2 = (radius * (1 + (P0[2] + t * direction[2]) / height))^2
        # Simplify and solve for t
        A = direction[0]**2 + direction[1]**2 - (radius * direction[2] / height)**2
        B = 2 * (P0[0] * direction[0] + P0[1] * direction[1] - (radius**2 / height) * (1 + P0[2] / height) * direction[2])
        C = P0[0]**2 + P0[1]**2 - (radius * (1 + P0[2] / height))**2

        # Solve the quadratic equation: A*t^2 + B*t + C = 0
        discriminant = B**2 - 4 * A * C
        if discriminant >= 0:
            t1 = (-B + np.sqrt(discriminant)) / (2 * A)
            t2 = (-B - np.sqrt(discriminant)) / (2 * A)
            # Filter valid solutions (z must be between -height_cutoff and 0)
            t_intersect = [t for t in [t1, t2] if t > 0]
            if t_intersect:
                # Calculate intersection points
                intersection_point = P0 + t_intersect[0] * direction
                intersection_points[ind] = intersection_point

                ommatidia_to_intersection[ind] = {
                    "om_dir": vert if isinstance(vert, list) else vert.tolist(),
                    "om_int": intersection_point.tolist(),
                    "t_intersect": t_intersect[0]
                }
            else:
                intersection_points[ind] = np.array([None]*3)
                ommatidia_to_intersection[ind] = {
                    "om_dir": vert if isinstance(vert, list) else vert.tolist(),
                    "om_int": [None]*3,
                    "t_intersect": None
                }
        else:
            intersection_points[ind] = np.array([None]*3)  # No intersection
            ommatidia_to_intersection[ind] = {
                "om_dir": vert if isinstance(vert, list) else vert.tolist(),
                "om_int": [None]*3,
                "t_intersect": None
            }
    return intersection_points, ommatidia_to_intersection
