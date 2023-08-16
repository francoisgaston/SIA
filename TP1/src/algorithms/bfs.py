from collections import deque
from algorithms.solver import Solver
from algorithms.solution import SSolution


class BFS(Solver):

    @staticmethod
    def solve(initial_state):
        queue = deque([initial_state])
        visited = {initial_state}
        visited_count = 0

        while queue:
            current_state = queue.popleft()

            if current_state.is_solution():
                return SSolution(visited_count, True, current_state)

            for next_state in current_state.explode():
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)

            visited_count += 1

        return SSolution(visited_count, False, None)

