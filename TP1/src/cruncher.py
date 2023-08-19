from data_structures.SokobanState import SokobanState
from algorithm_picker import Algorithm
from heuristic_picker import Heuristic
from input import read_input
import time
import sys
import json
import csv

def solve_sokoban(map_path, algorithm_name, heuristic_name):
    (map_limits, goal_points, boxes_position, player_coord, max_rows, max_cols, forbidden_points) = read_input(map_path)

    SokobanState.map_limits = map_limits
    SokobanState.goal_points = goal_points
    SokobanState.max_rows = max_rows
    SokobanState.max_cols = max_cols
    SokobanState.forbidden_points = forbidden_points
    state = SokobanState(None, 0, boxes_position, player_coord)

    solver = Algorithm.from_string(algorithm_name)
    heuristic = Heuristic.from_string(heuristic_name)
    start_time = time.time()
    solution = solver.solve(state, heuristic)
    end_time = time.time()

    return solution.visited_count, solution.end_state.steps if solution.is_valid() else float("inf"), end_time - start_time

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(sys.argv[1], "r") as file:
        config = json.load(file)

    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Map', 'Steps','Algorithm', 'Heuristic', 'Visited Count', 'End State Steps', 'Execution Time'])

        for map in config["maps"]:
            map_path = map[0]
            steps = map[1]
            print(f"Processing map: {map_path}")
            for algorithm_name in config["algorithm"]:
                print(f"  Algorithm: {algorithm_name}")
                for heuristic_name in config["heuristic"]:
                    print(f"    Heuristic: {heuristic_name}")
                    visited_count, end_state_steps, execution_time = solve_sokoban(map_path, algorithm_name, heuristic_name)
                    print(f"    Result: Visited Count = {visited_count}, End State Steps = {end_state_steps}, Execution Time = {execution_time:.2f}")
                    csv_writer.writerow([map_path, steps, algorithm_name, heuristic_name, visited_count, end_state_steps, execution_time])
    print("Done writing results to results.csv")

