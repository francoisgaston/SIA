class SokobanStatePath:

    def __init__(self, current_state, path):
        self.current_state = current_state
        self.path = path

    def __hash__(self):
        return hash((self.current_state, self.path))

    def __eq__(self, other):
        if isinstance(other, SokobanStatePath):
            return self.current_state == other.current_state and self.path == other.path
        return False

    def __lt__(self, other):
        if isinstance(other, SokobanStatePath):
            return self.current_state < other.current_state
        return NotImplemented

    def get_state(self):
        return self.current_state

    def get_path(self):
        return self.path

    def is_repeated(self, state):
        return state in self.path
