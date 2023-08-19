from data_structures.SokobanState import SokobanState


def rec_path_heuristic(state):
    # Genero una copia para no modificar el estado
    in_place = state.box_set.intersection(SokobanState.goal_points)
    goals = SokobanState.goal_points.difference(in_place)
    boxes = set(state.box_set.difference(in_place))
    player = state.player_coord

    return recursive_distance(player, boxes, goals)


def recursive_distance(point, eval_set, next_set):
    # Saco el punto (box, goal)
    next_set.discard(point)

    # Caso base
    if not len(eval_set) and not len(next_set):
        return 0

    # Menor distancia
    min_dist = SokobanState.max_rows + SokobanState.max_cols
    for x in eval_set:
        # distancia del resto menor
        aux = recursive_distance(x, set(next_set), set(eval_set))
        # distancia a evaluar
        aux += abs(point.row - x.row) + abs(point.col - x.col)
        if aux < min_dist:
            min_dist = aux

    return min_dist

