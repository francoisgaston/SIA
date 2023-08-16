from TP1.src.Point import Point
from TP1.src.SokobanState import SokobanState
from algorithms.bfs import BFS

# from input import read_input

if __name__ == "__main__":
    SokobanState.max_rows = 5
    SokobanState.max_cols = 5
    SokobanState.map_limits = {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3), Point(0,4),
                               Point(4,0),Point(4,1),Point(4,2),Point(4,3),Point(4,4),
                               Point(1,0),Point(2,0),Point(3,0),
                               Point(1,4),Point(2,4),Point(3,4)}
    SokobanState.goal_points = {Point(2, 3),Point(3,3)}
    state = SokobanState(None,0,{Point(2,2),Point(3,2)}, Point(2, 1))
    print(state)
    solution = BFS.solve(state)
    # print(solution.end_state)
    for curr in solution.build_solution():
        print(curr)


