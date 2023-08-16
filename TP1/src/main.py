from data_structures.Point import Point
from data_structures.SokobanState import SokobanState
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from input import read_input
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) <=1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols) = read_input(config["map"])
        SokobanState.map_limits = map_limits
        SokobanState.goal_points = goal_points
        SokobanState.max_rows = max_rows
        SokobanState.max_cols = max_cols
        state = SokobanState(None,0,boxes_position,player_coord)
        print(state)
        solution = BFS.solve(state)
        if solution.is_valid():
            for curr in solution.build_solution():
                print(curr)
        else:
            print("There is no solution for the map")
        print(solution.visited_count)
        print(solution.end_state.steps)

