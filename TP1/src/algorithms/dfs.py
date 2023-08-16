from solver import Solver
from solution import SSolution


class DFS(Solver):

    @staticmethod
    def solve(initial_state):
        queue = [initial_state]
        visited = {initial_state}
        visited_count = 0

        while queue:
            current_state = queue.pop()

            if current_state.is_solution():
                return SSolution(True, visited_count,current_state)

            for next_state in current_state.explode():
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)

            visited_count += 1

        return SSolution(False, visited_count,None)
