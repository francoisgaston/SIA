from algorithms.solver import Solver
from algorithms.solution import SSolution
import queue


class GREEDY(Solver):
    @staticmethod
    def solve(initial_state, heuristic):
        # PriorityQueue ordena por el primer valor, en empate por el segundo
        # ordena por heuristica, en empate por menor step
        border = queue.PriorityQueue()
        border.put((heuristic(initial_state), initial_state))
        # visited = {initial_state}
        visited = set()
        visited_count = 0

        while not border.empty():
            current_state = border.get()[1]

            if current_state.is_solution():
                return SSolution(visited_count, True, current_state)

            if current_state in visited:
                continue

            visited.add(current_state)

            for next_state in current_state.explode():
                if next_state not in visited:
                    # visited.add(next_state)
                    border.put((heuristic(next_state), next_state))

            visited_count += 1

        return SSolution(visited_count, False, None)
