from algorithms.solver import Solver
from algorithms.solution import SSolution
import queue


class AStar(Solver):

    @staticmethod
    def solve(initial_state, heuristic):
        border = queue.PriorityQueue()
        border.put((heuristic(initial_state), heuristic(initial_state), initial_state))
        # visited = {initial_state}
        visited = set()
        visited_count = 0

        while not border.empty():
            current_state = border.get()[2]

            if current_state.is_solution():
                return SSolution(visited_count, True, current_state, border.qsize())

            if current_state in visited:
                continue

            visited.add(current_state)

            for next_state in current_state.explode():
                if next_state not in visited:
                    # visited.add(next_state) #Esta mal, no lo marca como visitado cuando lo elije
                    # If f(n) are equal, tiebreak by h(n)
                    computed = heuristic(next_state)
                    border.put((computed + next_state.steps, computed, next_state))

            visited_count += 1

        return SSolution(visited_count, False, None, border.qsize())
