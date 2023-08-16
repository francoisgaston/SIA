from src.data_structures.Point import Point
from src.data_structures.SokobanState import SokobanState
import sys

def read_input(input):
    with open(input, 'r') as file:
        pos_y = 0
        pos_x = 0
        max_pos_x = 0
        map_limits = set()
        goal_points = set()
        boxes_position = set()
        player_coord = None
        while True:
            char = file.read(1)
            if char == '':  # Si el carácter leído está vacío => EOF
                break
            if char == '\n':
                pos_y += 1
                if pos_x > max_pos_x:
                    max_pos_x = pos_x
                pos_x = 0
            elif char == '#': # Wall
                map_limits.add(Point(pos_x, pos_y))
            elif char == '@': # Player
                if player_coord is not None:
                    raise Exception("More than one player")
                player_coord = Point(pos_x, pos_y)
            elif char == '+':  # Player on goal
                if player_coord is not None:
                    raise Exception("More than one player")
                player_coord = Point(pos_x, pos_y)
                goal_points.add(Point(pos_x, pos_y))
            elif char == '$':  # Box
                boxes_position.add(Point(pos_x, pos_y))
            elif char == '*':  # Box on goal
                boxes_position.add(Point(pos_x, pos_y))
                goal_points.add(Point(pos_x, pos_y))
            elif char == '.': # Goal
                goal_points.add(Point(pos_x, pos_y))
            pos_x += 1

        if len(boxes_position) != len(goal_points):
            raise Exception("Different numbers of boxes and goals")
        if player_coord is None:
            raise Exception("Player not found")

        return (map_limits, goal_points, boxes_position, player_coord, pos_y, max_pos_x)
##

## Main
if __name__ == "__main__":
    with open(f'{sys.argv[1]}', 'r') as config:
        (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols) = read_input(config["map"])
        SokobanState.map_limits = map_limits
        SokobanState.goal_points = goal_points
        SokobanState.max_rows = max_rows
        SokobanState.max_cols = max_cols

        state = SokobanState(None, 0, boxes_position, player_coord)
        print(state)
