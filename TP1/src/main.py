from Point import Point
from SokobanState import SokobanState

if __name__ == "__main__":
    SokobanState.max_rows = 4
    SokobanState.max_cols = 4
    SokobanState.map_limits = {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)}
    SokobanState.goal_points = {Point(1, 1),Point(2, 3)}
    state = SokobanState(None,0,{Point(1, 2),Point(2,2)}, Point(2, 1))
    print(state)
    for curr in state.explode():
        print(curr)