from data_structures.SokobanState import SokobanState
from algorithm_picker import Algorithm
from heuristic_picker import Heuristic
from input import read_input
from utils import write_to_txt
import sys
import json

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols, forbidden_points) = read_input(config["map"])

        SokobanState.map_limits = map_limits
        SokobanState.goal_points = goal_points
        SokobanState.max_rows = max_rows
        SokobanState.max_cols = max_cols
        if config["forbidden_points"] == "YES":
            SokobanState.forbidden_points = forbidden_points
        else:
            SokobanState.forbidden_points = set()
        state = SokobanState(None, 0, boxes_position, player_coord)

        solver = Algorithm.from_string(config["algorithm"])
        heuristic = Heuristic.from_string(config["heuristic"])
        solution = solver.solve(state, heuristic)

        if solution.is_valid():
            printable_solution = []
            for curr in solution.build_solution():
                printable_solution.append(curr)
            write_to_txt(config["output"], "\n".join(printable_solution))
        else:
            print("There is no solution for the map")


