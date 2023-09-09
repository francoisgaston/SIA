import sys
import json
import csv
import os
import numpy as np
from datetime import datetime
from main import run_genetic


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the config file.")
        sys.exit(1)

    boltzmann_config = sys.argv[1]

    with open(f"{boltzmann_config}", "r") as file:
        config = json.load(file)
        ans = []
        test_params = config[config["test"]]
        for value in np.arange(test_params["start"], test_params["end"] + test_params["step"], test_params["step"]):
            print(f"Running for {value}")
            selection = {
                "name": "BOLTZMANN",
            }
            if config["test"] == "k":
                selection["tc"] = config["default_Tc"]
                selection["t0"] = config["default_T0"]
                selection["c"] = value
            elif config["test"] == "T0":
                selection["tc"] = config["default_Tc"]
                selection["t0"] = value
                selection["c"] = config["default_k"]
            elif config["test"] == "Tc":
                selection["tc"] = value
                selection["t0"] = config["default_T0"]
                selection["c"] = config["default_k"]
            else:
                raise ValueError("Invalid test parameter")

            for i in range(config["times"]):
                print(f"Running for {i}")

                ans += run_genetic(
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

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = config["output"] + "_" + config["test"] + "_" + timestamp + ".csv"
        os.makedirs(os.path.dirname(CSV), exist_ok=True)
        file = open(CSV, 'w', newline='')
        writer = csv.writer(file)

        header = ["fitness", "attack", "defense", "height", "agility_items", "strength_items",
                    "resistance_items", "expertise_items", "life_items",
                    "individual_class", "crossover", "population_0_count", "selection_1", "selection_2",
                    "replace_1", "replace_2","replace_type", "mutation", "mutation_probability", "stop_condition",
                    "K", "A", "B", "id"]

        writer.writerow(header)
        writer.writerows(ans)
        file.close()
