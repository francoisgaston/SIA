from algorithms.solver import Solver
from algorithms.solution import SSolution
from algorithms.distance_heuristic import distance_heuristic
import queue


class AStar(Solver):

    @staticmethod
    def solve(initial_state):
        border = queue.PriorityQueue()
        border.put((distance_heuristic(initial_state), initial_state))
        visited = {initial_state}
        visited_count = 0

        while border:
            current_state = border.get()

            if current_state[1].is_solution():
                return SSolution(visited_count, True, current_state[1])

            for next_state in current_state[1].explode():
                if next_state not in visited:
                    visited.add(next_state)
                    border.put((distance_heuristic(next_state) + next_state.steps, next_state))

            visited_count += 1

        return SSolution(visited_count, False, None)
