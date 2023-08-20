import numpy as np
# from heuristic import Heuristics 
from data_structures.SokobanState import SokobanState



class CosineHeuristic():
    steps = 0
    @staticmethod
    def set_to_vector(box_set, max_rows, max_cols):
        vector = np.ones(max_rows * max_cols)
        for point in box_set:
            index = point.row * max_cols + point.col
            vector[index] = 0
        return vector

    @staticmethod
    def apply(state):
        initial_vector = CosineHeuristic.set_to_vector(state.box_set, SokobanState.max_rows, SokobanState.max_cols)
        final_vector = CosineHeuristic.set_to_vector(state.goal_points, SokobanState.max_rows, SokobanState.max_cols)

        similarity = np.dot(initial_vector, final_vector)
        cosine_distance = similarity / (np.linalg.norm(initial_vector) * np.linalg.norm(final_vector))
        CosineHeuristic.steps += 1
        return (1 - cosine_distance) * CosineHeuristic.steps

