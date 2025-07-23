import numpy as np

from fovmap.plots_utils import plot_candidates, plot_candidates_and_selected, plot_everything


def angle_threshold_input():
    wrong_input = True
    while wrong_input:
        # selection is not correct manually increase the threshold
        threshold_input = input("Enter the threshold angle: ")
        try:
            angle_threshold = float(threshold_input)
            wrong_input = False
        # except ValueError to avoid false input
        except ValueError:
            print("Please enter a valid float number")
    return angle_threshold


def find_similar_vectors_from_vector(vector, angle_threshold, vectors):
    cos_threshold = np.cos(np.radians(angle_threshold))  # Convert threshold to cosine

    similar = []
    for u in vectors:
        if vector != u:
            cosine_sim = np.dot(vector, u) / (np.linalg.norm(vector) * np.linalg.norm(u))
            if cosine_sim > cos_threshold:  # Angle is smaller than threshold
                similar.append(u)

    return similar


def manual_hex_segmentation(
   current_cp,
   cps_vertices,
   hgps_vertices,
   edge_vertices,
   vertices_wo_cps_edges,
   vertices_wo_cps_hgps_edges,
   cp_sel_angle_threshold,
   hgps_sel_angle_threshold,
   n_center,
   ommatidia_hex_grid
   ):
    try:
        while len(vertices_wo_cps_hgps_edges) != 0:
            if n_center == 0:
                new_current_cp = current_cp
                # find next point to be center
            else:
                print("find next cp")
                # initialize variables
                are_cps_sel_correct = False
                is_cp_sel_correct = False
                cp_angle_threshold = cp_sel_angle_threshold
                while not are_cps_sel_correct and not is_cp_sel_correct:  # in case the user needs to reselect the points
                    while not are_cps_sel_correct:  # while the selection is not correct
                        # show the points surroundint the current center point
                        cp_surr_points = find_similar_vectors_from_vector(
                            current_cp,
                            cp_angle_threshold,
                            vertices_wo_cps_hgps_edges
                            )
                        if len(cp_surr_points) == 0:
                            print("No points found, please increase the threshold angle")
                            # selection is not correct manually increase the threshold
                            cp_angle_threshold = angle_threshold_input()
                        else:  # there are candidates
                            # remove candidates to remaining for now
                            cp_sel_remaining_points = vertices_wo_cps_hgps_edges.copy()
                            for cp_surr_point in cp_surr_points:
                                if cp_surr_point in cp_sel_remaining_points:
                                    cp_sel_remaining_points.remove(cp_surr_point)
                            # plot the points
                            plot_candidates(
                                current_cp,  # current center point
                                cp_surr_points,  # candidates to be the next center point
                                cps_vertices,  # already defined center points
                                hgps_vertices,  # already defined hex grid points
                                cp_sel_remaining_points,  # remaining points
                                edge_vertices  # edges
                                )

                            # ask the user if the selection is correct
                            correct_cps_candidates_sel = input("Is the selection correct? (y/n)")
                            if correct_cps_candidates_sel == "y":
                                are_cps_sel_correct = True  # escape the loop
                                selected_cps_candidates = cp_surr_points
                            elif correct_cps_candidates_sel == "n":
                                # selection is not correct manually increase the threshold
                                cp_angle_threshold = angle_threshold_input()

                    # decide whether to keep the surrounding points
                    while not is_cp_sel_correct:
                        cp_input = input("Enter the index of the point you want to select (enter esc to go back to previous step): ")
                        if cp_input == "esc":
                            are_cps_sel_correct = False
                            break
                        try:
                            # get selected point from the input
                            cp_index = int(cp_input)
                            cp_selected = selected_cps_candidates[cp_index]
                            # remove candidates from remaining for now
                            cp_sel_remaining_points = vertices_wo_cps_hgps_edges.copy()
                            for selected_cps_candidate in selected_cps_candidates:
                                if selected_cps_candidate in cp_sel_remaining_points:
                                    cp_sel_remaining_points.remove(selected_cps_candidate)
                            # remove the selected point from the candidates
                            candidates_copy = selected_cps_candidates.copy()
                            candidates_copy.remove(cp_selected)
                            # plot the points
                            plot_candidates_and_selected(
                                current_cp,
                                cp_selected,
                                candidates_copy,
                                cps_vertices,
                                hgps_vertices,
                                cp_sel_remaining_points,
                                edge_vertices
                                )
                            # ask if the selected center point should be the next center point
                            # this is also the time to remove the edges from the list
                            is_this_cp_good = input("Is this the next cp? (y/n/e to add to edges)")
                            if is_this_cp_good == "y":
                                new_current_cp = cp_selected
                                is_cp_sel_correct = True
                            if is_this_cp_good == "e":
                                edge_vertices.append(cp_selected)
                                if cp_selected in vertices_wo_cps_hgps_edges:
                                    vertices_wo_cps_hgps_edges.remove(cp_selected)
                                if cp_selected in vertices_wo_cps_edges:
                                    vertices_wo_cps_edges.remove(cp_selected)
                                selected_cps_candidates.remove(cp_selected)
                        # except ValueError to avoid false input
                        except ValueError:
                            print("Please enter a valid integer")
                        except IndexError:
                            print(f"Please enter a valid index, list has length {len(selected_cps_candidates)}")

            # cp found, found surrounding points
            print("find next hg points")
            is_hgps_selection_correct = False
            threshold_angle = hgps_sel_angle_threshold
            hgps_found = False
            while not is_hgps_selection_correct and not hgps_found:
                while not is_hgps_selection_correct:
                    # find surrounding points candidates
                    hg_surr_points = find_similar_vectors_from_vector(
                        new_current_cp,
                        threshold_angle,
                        vertices_wo_cps_edges
                        )
                    if len(hg_surr_points) == 0:
                        print("No points found, please increase the threshold angle")
                        # selection is not correct manually increase the threshold
                        threshold_angle = angle_threshold_input()
                    else:  # there are candidates
                        # remove candidates from remaining for now
                        hg_sel_remaining_points = vertices_wo_cps_hgps_edges.copy()
                        for hg_surr_point in hg_surr_points:
                            if hg_surr_point in hg_sel_remaining_points:
                                hg_sel_remaining_points.remove(hg_surr_point)
                        # plot the points
                        plot_candidates(
                            new_current_cp,
                            hg_surr_points,  # candidates
                            cps_vertices,
                            hgps_vertices,
                            hg_sel_remaining_points,
                            edge_vertices
                            )
                        # ask the user if the selection is correct
                        correct_hgs_candidates_sel = input("Is the selection correct? (y/n)")
                        if correct_hgs_candidates_sel == "y":
                            is_hgps_selection_correct = True
                            selected_hgps_candidates = hg_surr_points
                        elif correct_hgs_candidates_sel == "n":
                            threshold_angle = angle_threshold_input()

                # decide whether to keep the surrounding points
                while not hgps_found:
                    if not is_hgps_selection_correct:
                        break
                    # remove candidates from remaining for now
                    # recompute every time for hg_surr_points updates
                    hg_sel_remaining_points = vertices_wo_cps_hgps_edges.copy()
                    for selected_hgps_candidate in selected_hgps_candidates:
                        if selected_hgps_candidate in hg_sel_remaining_points:
                            hg_sel_remaining_points.remove(selected_hgps_candidate)
                    plot_candidates(
                        new_current_cp,
                        selected_hgps_candidates,
                        cps_vertices,
                        hgps_vertices,
                        hg_sel_remaining_points,
                        edge_vertices
                        )
                    keep_points = input("Do you want to keep the surrounding points? (y/n)")
                    if keep_points == "y":
                        ommatidia_hex_grid[n_center] = {
                            "center": new_current_cp,
                            "surrounding": selected_hgps_candidates
                        }
                        print(
                            f"""
                            Index: {n_center}\n
                            center point: {new_current_cp}\n
                            surrounding points: {selected_hgps_candidates}
                            """
                             )
                        n_center += 1
                        # remove the center point and surrounding points from the lists
                        vertices_wo_cps_hgps_edges.remove(new_current_cp)
                        vertices_wo_cps_edges.remove(new_current_cp)
                        for selected_hgps_candidate in selected_hgps_candidates:
                            if selected_hgps_candidate in vertices_wo_cps_hgps_edges:
                                vertices_wo_cps_hgps_edges.remove(selected_hgps_candidate)
                            # add the selected points to the list of hgps
                            if selected_hgps_candidate not in hgps_vertices:
                                hgps_vertices.append(selected_hgps_candidate)
                        # add the center point to the list of cps
                        cps_vertices.append(new_current_cp)
                        # update current_cp for next iteration
                        current_cp = new_current_cp
                        hgps_found = True

                    elif keep_points == "n":
                        correct_point_selected = False
                        while not correct_point_selected:
                            hg_input = input("Enter the index of the point you want to remove (enter esc to go back to previous step): ")
                            if hg_input == "esc":
                                is_hgps_selection_correct = False
                                break
                            # else
                            try:
                                hg_index = int(hg_input)
                                selected_hg = selected_hgps_candidates[hg_index]
                                # remove candidates to remaining for now
                                hg_sel_remaining_points = vertices_wo_cps_hgps_edges.copy()
                                for selected_hgps_candidate in selected_hgps_candidates:
                                    if selected_hgps_candidate in hg_sel_remaining_points:
                                        hg_sel_remaining_points.remove(selected_hgps_candidate)
                                # remove the selected point from the candidates
                                hg_candidates_copy = selected_hgps_candidates.copy()
                                hg_candidates_copy.remove(selected_hg)
                                # plot the points
                                plot_candidates_and_selected(
                                    new_current_cp,
                                    selected_hg,
                                    hg_candidates_copy,
                                    cps_vertices,
                                    hgps_vertices,
                                    hg_sel_remaining_points,
                                    edge_vertices
                                    )

                                remove_this_point = input("Is this the correct point to remove? (y/n)")
                                if remove_this_point == "y":
                                    selected_hgps_candidates = hg_candidates_copy
                                    more_points_to_remove = input("Do you want to remove more points? (y/n)")
                                    if more_points_to_remove == "n":
                                        correct_point_selected = True
                                elif remove_this_point == "esc":
                                    correct_point_selected = True
                            # except ValueError to avoid false input
                            except ValueError:
                                print("Please enter a valid integer")
                            except IndexError:
                                print(f"Please enter a valid index, list has length {len(selected_hgps_candidates)}")
        print("All points have been assigned to cps, hgps or edges")
        print(f"Number of center points: {len(cps_vertices)}")
        print(f"Number of hex grid points: {len(hgps_vertices)}")
        print(f"Number of edge points: {len(edge_vertices)}")
        return (
            current_cp,
            cps_vertices,
            hgps_vertices,
            edge_vertices,
            vertices_wo_cps_edges,
            vertices_wo_cps_hgps_edges,
            cp_sel_angle_threshold,
            hgps_sel_angle_threshold,
            n_center,
            ommatidia_hex_grid
            )

    except KeyboardInterrupt:
        are_cps_sel_correct = False
        is_cp_sel_correct = False
        is_hgps_selection_correct = False
        hgps_found = False
        return (
            current_cp,
            cps_vertices,
            hgps_vertices,
            edge_vertices,
            vertices_wo_cps_edges,
            vertices_wo_cps_hgps_edges,
            cp_sel_angle_threshold,
            hgps_sel_angle_threshold,
            n_center,
            ommatidia_hex_grid
            )


def manual_labeling(
   results,
   already_labeled,
   to_be_labeled,
   labels,
   colors
   ):
    while len(to_be_labeled) != 0:
        current_cp = to_be_labeled[0]  # get the first point to be labeled
        plot_everything(
            current_cp,
            already_labeled,
            to_be_labeled,
            results,
            colors
            )
        not_valid_input = True
        while not_valid_input:
            selected_label_int = input(f"Enter the label index for the current point {labels}")
            try:
                selected_label = int(selected_label_int)
                not_valid_input = False
            except ValueError:
                print("Please enter a valid integer")
        results[str(current_cp)] = labels[selected_label]
        already_labeled.append(current_cp)
        to_be_labeled.remove(current_cp)
    return results, already_labeled, to_be_labeled
