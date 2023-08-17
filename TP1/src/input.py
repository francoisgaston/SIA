from data_structures.Point import Point


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
            while char != '' and char != '\n':
                match char:
                    case '#':  # Wall
                        map_limits.add(Point(pos_y, pos_x))
                    case '@':  # Player
                        if player_coord is not None:
                            raise Exception("More than one player")
                        player_coord = Point(pos_y, pos_x)
                    case '+':  # Player on goal
                        if player_coord is not None:
                            raise Exception("More than one player")
                        player_coord = Point(pos_y, pos_x)
                        goal_points.add(Point(pos_y, pos_x))
                    case '$':  # Box
                        boxes_position.add(Point(pos_y, pos_x))
                    case '*':  # Box on goal
                        boxes_position.add(Point(pos_y, pos_x))
                        goal_points.add(Point(pos_y, pos_x))
                    case '.':  # Goal
                        goal_points.add(Point(pos_y, pos_x))
                pos_x += 1
                char = file.read(1)
            pos_y += 1
            if pos_x > max_pos_x:
                max_pos_x = pos_x
            if char == '':
                break
            else:
                pos_x = 0

        if len(boxes_position) != len(goal_points):
            raise Exception("Different numbers of boxes and goals")
        if player_coord is None:
            raise Exception("Player not found")

        return map_limits, goal_points, boxes_position, player_coord, pos_y, max_pos_x
