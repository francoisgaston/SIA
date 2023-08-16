from Point import Point

class SokobanState:
    # hola joseshito

    # Change when game starts
    map_limits = set()
    goal_points = set()
    max_rows = 0
    max_cols = 0

    def __init__(self, parent, steps, box_points, player_coord):
        self.parent = parent
        self.steps = steps
        self.box_set = box_points
        self.player_coord = player_coord

    def __hash__(self):
        return hash((self.box_set,self.player_coord))

    def __eq__(self, other):
        if isinstance(other, SokobanState):
            return self.box_set == other.box_set and self.player_coord == other.player_coord
        return False

    def __str__(self):
        ans = "|" # Horrible concatenar tantos strings, pero despues lo vemos
        for _ in range(SokobanState.max_cols):
            ans += "--"
        ans += "|\n|"
        for row in range(SokobanState.max_rows):
            for col in range(SokobanState.max_cols):
                p = Point(row,col)
                if p in SokobanState.goal_points and p in self.box_set:
                    ans += 'G' # Poner 🥅
                elif p in SokobanState.goal_points and p == self.player_coord:
                    ans += '$'
                elif p in SokobanState.goal_points:
                    ans += '.'
                elif p in SokobanState.map_limits:
                    ans += 'X'
                elif p in self.box_set:
                    ans += 'B'
                elif p == self.player_coord:
                    ans += 'P'
                else:
                    ans += ' '
                ans += ' '
            ans += "|\n|"""# Termina una fila
        for _ in range(SokobanState.max_cols):
            ans += '--'
        ans += "|\n"
        return ans


    def explode(self):
        dirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        valid_moves = []

        for dir in dirs:
            new_player_coord = self.player_coord.move(dir[0], dir[1])
            new_box_state = set(self.box_set)
            if new_player_coord in self.box_set:
                #mueve una caja en la misma direccion de la persona
                new_box_state.remove(new_player_coord)
                new_box_state.add(new_player_coord.move(dir[0], dir[1]))
            new_state = SokobanState(self, self.steps + 1, new_box_state, new_player_coord)
            if new_state.is_valid_state():
                valid_moves.append(new_state)
        return valid_moves

    def is_valid_state(self):
        if self.player_coord in SokobanState.map_limits:
            return False
        if self.player_coord in self.box_set:
            return False
        if len(self.box_set) != len(SokobanState.goal_points):
            # Una caja piso a otra
            return False
        for box in self.box_set:
            if box in SokobanState.map_limits:
                return False
        return True

    def is_solution(self):
        return self.box_set == SokobanState.goal_points
