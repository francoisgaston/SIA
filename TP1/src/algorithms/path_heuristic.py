from data_structures.SokobanState import SokobanState


def path_heuristic(state):
    total_dist = 0

    # Genero una copia para no modificar el estado
    in_place = state.box_set.intersection(SokobanState.goal_points)
    goals = SokobanState.goal_points.difference(in_place)
    boxes = set(state.box_set.difference(in_place))

    if len(boxes) == 0:
        return 0

    near_box = None
    near_goal = None
    player_dist = SokobanState.max_rows + SokobanState.max_cols


    # Distancia player-box
    for box in boxes:
        player_aux_dist = abs(state.player_coord.row - box.row) + abs(state.player_coord.col - box.col)
        if player_aux_dist < player_dist:
            player_dist = player_aux_dist
            near_box = box
    total_dist += player_dist
    boxes.remove(near_box)

    # Distancia box-goal + goal-box
    while boxes:

        # distancia box-goal
        goal_dist = SokobanState.max_rows + SokobanState.max_cols
        for goal in goals:
            goal_aux_dist = abs(goal.row - near_box.row) + abs(goal.col - near_box.col)
            if goal_aux_dist < goal_dist:
                goal_dist = goal_aux_dist
                near_goal = goal
        total_dist += goal_dist
        goals.remove(near_goal)

        # distancia goal-box
        box_dist = SokobanState.max_rows + SokobanState.max_cols
        for box in boxes:
            box_aux_dist = abs(box.row - near_goal.row) + abs(box.col - near_goal.col)
            if box_aux_dist < box_dist:
                box_dist = box_aux_dist
                near_box = box
        total_dist += box_dist
        boxes.remove(near_box)

    return total_dist
