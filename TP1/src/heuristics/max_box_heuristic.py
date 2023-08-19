from data_structures.SokobanState import SokobanState


# NO FUNCIONA
#
def max_box_heuristic(state):
    ans = 0
    for box in state.box_set:
        if box in SokobanState.goal_points:
            continue
        aux = abs(state.player_coord.row - box.row) + abs(state.player_coord.col - box.col)
        # Suma distancias box-goal
        if aux > ans:
            ans = aux
    return ans
