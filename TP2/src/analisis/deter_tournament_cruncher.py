import json
import sys
import csv
import os
from datetime import datetime
from main import run_genetic


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the config file.")
        sys.exit(1)

    tournament_config = sys.argv[1]

    with open(f"{tournament_config}", "r") as file:
        config = json.load(file)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = config["output"] + "_" + timestamp + ".csv"
        os.makedirs(os.path.dirname(CSV), exist_ok=True)
        file = open(CSV, 'w', newline='')
        writer = csv.writer(file)

        header = ["fitness", "attack", "defense", "height", "agility_items", "strength_items",
                  "resistance_items", "expertise_items", "life_items",
                  "individual_class", "crossover", "population_0_count", "selection_1", "selection_2",
                  "replace_1", "replace_2", "replace_type", "mutation", "mutation_probability", "stop_condition",
                  "K", "A", "B", "id"]

        writer.writerow(header)

        ans = []
        test_params = config["m"]
        for value in range(test_params["start"], test_params["end"] + test_params["step"], test_params["step"]):
            print(f"Running for {value}")
            selection = {
                "name": "DETER_TOURNAMENT",
                "m": value
            }
            for i in range(config["times"]):
                print(f"Running for {i}")
                ans = run_genetic(
                    individual_class=config["class"],
                    crossover=config["crossover"],
                    population_0_count=config["population_0_count"],
                    selection_1=selection,
                    replace_1=selection,
                    replace=config["replace"],
                    mutation=config["mutation"],
                    mutation_probability=config["mutation_probability"],
                    stop_condition=config["stop_condition"],
                    stop_condition_options=config["stop_condition_options"],
                    K=config["K"],
                    A=config["A"],
                    B=config["B"],
                    last_generation_count=1,
                    id=value)

                writer.writerows(ans)

        file.close()
