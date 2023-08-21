from collections import deque
from algorithms.solver import Solver
from algorithms.solution import SSolution


class BFS(Solver):

    @staticmethod
    def solve(initial_state, _):
        queue = deque([initial_state])
        visited = set()
        visited_count = 0

        while queue:
            current_state = queue.popleft()
            if current_state.is_solution():
                return SSolution(visited_count, True, current_state, len(queue))
            if current_state in visited:
                continue
            visited.add(current_state)
            for next_state in current_state.explode():
                queue.append(next_state)

            visited_count += 1

        return SSolution(visited_count, False, None, len(queue))
