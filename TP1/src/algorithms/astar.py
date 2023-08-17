from algorithms.solver import Solver
from algorithms.solution import SSolution
import queue


class AStar(Solver):

    @staticmethod
    def solve(initial_state, heuristic):
        border = queue.PriorityQueue()
        border.put((heuristic(initial_state), heuristic(initial_state), initial_state))
        visited = {initial_state}
        visited_count = 0

        while border:
            current_state = border.get()[2]

            if current_state.is_solution():
                return SSolution(visited_count, True, current_state)

            for next_state in current_state.explode():
                if next_state not in visited:
                    visited.add(next_state)
                    # If f(n) are equal, tiebreak by h(n)
                    border.put((heuristic(next_state) + next_state.steps, heuristic(next_state), next_state))

            visited_count += 1

        return SSolution(visited_count, False, None)
