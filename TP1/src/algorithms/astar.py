from algorithms.solver import Solver
from algorithms.solution import SSolution
from data_structures.SokobanStatePath import SokobanStatePath
import queue


class AStar(Solver):

    @staticmethod
    def solve(initial_state, heuristic):
        border = queue.PriorityQueue()
        border.put((
            heuristic(initial_state),
            heuristic(initial_state),
            SokobanStatePath(initial_state, {initial_state})
        ))
        visited_count = 0

        while not border.empty():
            current_state_path = border.get()[2]
            current_state = current_state_path.get_state()
            current_path = current_state_path.get_path()

            if current_state.is_solution():
                return SSolution(visited_count, True, current_state)

            for next_state in current_state.explode():
                if current_state_path.is_repeated(next_state):
                    continue
                next_path = set(current_path.copy())
                next_path.add(next_state)
                computed_heuristic = heuristic(next_state)
                border.put((
                    computed_heuristic + next_state.steps,
                    computed_heuristic,
                    SokobanStatePath(next_state, next_path)
                ))
            visited_count += 1

        return SSolution(visited_count, False, None)
