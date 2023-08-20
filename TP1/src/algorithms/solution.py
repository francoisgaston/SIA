class SSolution:
    def __init__(self, visited_count, valid, end_state, frontier_count):
        self.visited_count = visited_count
        self.valid = valid
        self.end_state = end_state
        self.frontier_count = frontier_count
    def is_valid(self):
        return self.valid

    def build_solution(self):
        solution_path = []
        state = self.end_state
        while state:
            solution_path.append(state)
            state = state.parent
        return reversed(solution_path)