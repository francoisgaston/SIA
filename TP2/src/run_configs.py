import csv
import sys
import json
import os
from main import run_genetic
from datetime import datetime

# Le pasas los configs que queres correr y comparar y genera 2 CSV:
# 1) Datos de la ultimas generaciones para cada config
# 2) Datos de todas las generaciones de cada corrida => si no lo queres fulldata=False
# Ej: python3 src/run_configs.py src/config/config.json src/config/min_config.json 
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    ans = []
    properties_fulldata = []
    context_count = 0
    counter_args = 0
    iterations_for_error = 5

    for context in sys.argv:

        # No considerar el 1er argumento
        counter_args += 1
        if counter_args == 1:
            continue

        context_count += 1
        with open(f"{context}", "r") as file:
            config = json.load(file)
            for classs in ["WARRIOR","ARCHER", "INFILTRATE", "DEFENDER"]:
                for i in range(iterations_for_error):
                    aux_ans, aux_properties_fulldata = run_genetic(individual_class=classs,
                                                                crossover=config["crossover"],
                                                                population_0_count=config["population_0_count"],
                                                                selection_1=config["selection_1"],
                                                                selection_2=config["selection_2"],
                                                                replace_1=config["replace_1"],
                                                                replace_2=config["replace_2"],
                                                                replace=config["replace"],
                                                                mutation=config["mutation"],
                                                                mutation_probability=config["mutation_probability"],
                                                                stop_condition=config["stop_condition"],
                                                                stop_condition_options=config["stop_condition_options"],
                                                                K=config["K"],
                                                                A=config["A"],
                                                                B=config["B"],
                                                                last_generation_count=1,
                                                                id=" ".join(context.split("/")[-1].split(".")[0].split("_")).title(),
                                                                fulldata=True)
                    ans += aux_ans
                    properties_fulldata += aux_properties_fulldata
                    print(f'ready {i} {context} {classs}')

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

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    CSV = config["output"] + "fulldata_" + timestamp + ".csv"
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    file = open(CSV, 'w', newline='')
    writer = csv.writer(file)

    header = ["agility", "strength", "resistance", "expertise", "life", "height", "fitness", "id", "generations", "id_config", "class"]

    writer.writerow(header)
    writer.writerows(properties_fulldata)

    file.close()