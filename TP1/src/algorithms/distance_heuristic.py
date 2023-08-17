from data_structures.SokobanState import SokobanState


# No es optima, deberiamos ver cual es la suma menor de cada una
def distance_heuristic(state):
    total_dist = 0
    player_dist = SokobanState.max_rows + SokobanState.max_cols

    for box in state.box_set:

        # Suma distancias box-goal
        box_goal_dist = SokobanState.max_rows + SokobanState.max_cols
        for goal in SokobanState.goal_points:
            aux_dist = abs(goal.row - box.row) + abs(goal.col - box.col)
            if aux_dist < box_goal_dist:
                box_goal_dist = aux_dist
        total_dist += box_goal_dist

        # Menor distancia box-player
        player_aux_dist = abs(state.player_coord.row - box.row) + abs(state.player_coord.col - box.col)
        if player_aux_dist < player_dist:
            player_dist = player_aux_dist

    return total_dist + player_dist
