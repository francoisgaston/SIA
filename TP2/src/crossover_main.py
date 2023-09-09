import csv
import sys
import json
import os
from main import run_genetic
from datetime import datetime
from fitness import Fitness
from mutation import MutationEngine
from individual import Individual, ItemProp
from crossover import Crossover
from algorithm import generate_initial_population, GenerationState
from selection import Selection
from replace import Replace


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    ans = []
    id = 0
    counter_args = 0
    iterations_for_error = 5

    for context in sys.argv:

        # No considerar el 1er argumento
        counter_args += 1
        if counter_args == 1:
            continue

        id += 1
        with open(f"{context}", "r") as file:
            config = json.load(file)
            for method in ["UNIFORM_POINT", "ANULAR", "SINGLE_POINT", "TWO_POINT"]:
                for i in range(iterations_for_error):
                    ans += run_genetic(individual_class=config["class"], crossover=method,
                                population_0_count=config["population_0_count"],
                                selection_1=config["selection_1"], selection_2=config["selection_2"],
                                replace_1=config["replace_1"],
                                replace_2=config["replace_2"], replace=config["replace"],
                                mutation=config["mutation"], mutation_probability=config["mutation_probability"],
                                stop_condition=config["stop_condition"],
                                stop_condition_options=config["stop_condition_options"],
                                K=config["K"], A=config["A"], B=config["B"],
                                last_generation_count=1, id = id)
                    print(f'ready {i} {method} {context}')


    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    CSV = config["output"] + "_" + timestamp + ".csv"
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