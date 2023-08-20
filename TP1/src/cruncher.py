from data_structures.SokobanState import SokobanState
from algorithm_picker import Algorithm
from heuristic_picker import Heuristic
from input import read_input
from utils import write_to_csv
import time
import sys
import json


def solve_sokoban(map_path, algorithm_name, heuristic_name, do_forbidden_points):
    (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols, forbidden_points) = read_input(map_path)

    SokobanState.map_limits = map_limits
    SokobanState.goal_points = goal_points
    SokobanState.max_rows = max_rows
    SokobanState.max_cols = max_cols
    if do_forbidden_points == True:
        SokobanState.forbidden_points = forbidden_points
    else: 
        SokobanState.forbidden_points = set()
    state = SokobanState(None, 0, boxes_position, player_coord)

    solver = Algorithm.from_string(algorithm_name)
    heuristic = Heuristic.from_string(heuristic_name)
    start_time = time.time()
    solution = solver.solve(state, heuristic)
    end_time = time.time()

    return solution.visited_count, solution.end_state.steps if solution.is_valid() else float("inf"), solution.frontier_count, end_time - start_time

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(sys.argv[1], "r") as file:
        config = json.load(file)

        csv_rows = [["Map", "n-th map", "Algorithm", 'Heuristic', 'Visited Count', 'End State Steps', 'Frontier Count',
                     'Execution Time']]
        map_count = 0

        for map in config["maps"]:
            map_count += 1
            print(f"Processing map: {map}")
            for algorithm_name in config["algorithms"]:
                print(f"  Algorithm: {algorithm_name}")
                for heuristic_name in config["heuristics"]:
                    print(f"    Heuristic: {heuristic_name}")
                    visited_count, end_state_steps, frontier_count, execution_time = solve_sokoban(map, algorithm_name, heuristic_name, config["forbidden_points"] == "YES")
                    print(f"    Result: Visited Count = {visited_count}, End State Steps = {end_state_steps}, Frontier Count = {frontier_count}, Execution Time = {execution_time:.2f}")
                    csv_rows.append([map, map_count, algorithm_name, heuristic_name, visited_count, end_state_steps, frontier_count, execution_time])
        write_to_csv(config["output"], csv_rows)
    print("Done writing results to csv file")

