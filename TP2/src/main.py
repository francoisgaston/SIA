import csv
import sys
import json
import os
from datetime import datetime
from fitness import Fitness
from mutation import MutationEngine
from individual import Individual, ItemProp
from crossover import Crossover
from algorithm import generate_initial_population, GenerationState
from selection import Selection
from replace import Replace


# last_generation_count: cuantos imprime de la generación final
# id: opcional para identificar una ejecución del algoritmo
# Return: lista de tuplas con todos los valores relevantes

def run_genetic(individual_class="WARRIOR", crossover="ANULAR", population_0_count=100,
                selection_1=None, selection_2=None, replace_1=None, repeat_in_selection=False,
                replace_2=None, replace="SESGO", mutation="MULTI_GEN_UNIFORM", max_generations=10,
                stop_condition="max_generations", stop_condition_options=None,
                mutation_probability=0.5, K=100, A=0.5, B=0.5, last_generation_count=3, id=1):
    # Defaults para objetos (estan aca porque si no se queja de que el default es mutable)
    if replace_2 is None:
        replace_2 = {
            "name": "BOLTZMANN",
            "tc": 10,
            "t0": 50,
            "c": 1
        }
    if stop_condition_options is None:
        stop_condition_options = {
            "max_generations": 1000,
            "max_time": 0.1,
            "acceptable_solution": 1
        }
    if replace_1 is None:
        replace_1 = {
            "name": "ELITE",
            "m": 5
        }
    if selection_2 is None:
        selection_2 = {
            "name": "UNIVERSAL",
            "tc": 10,
            "t0": 50,
            "c": 1
        }
    if selection_1 is None:
        selection_1 = {"name": "ROULETTE", "m": 5}
    if K % 2 != 0:  # TODO: cambiar si aceptamos que K sea impar
        raise ValueError

    Individual.FITNESS_FUNCTION = Fitness.from_string(individual_class)
    Individual.CROSSOVER_FUNCTION = Crossover.from_string(crossover)
    population_size = population_0_count
    selection_method_1 = Selection.get_selection_method(selection_1)
    selection_method_2 = Selection.get_selection_method(selection_2)
    replace_method_1 = Selection.get_selection_method(replace_1)
    replace_method_2 = Selection.get_selection_method(replace_2)
    replace_method = Replace.from_string(replace)
    mutation_method = MutationEngine.from_string(mutation)
    MutationEngine.MUTATION_PROBABILITY = mutation_probability
    Selection.REPEAT_IN_SELECTION = repeat_in_selection
    generation_state = GenerationState(stop_condition, stop_condition_options)
    # Generacion 0
    population = generate_initial_population(population_size)
    generations = 0
    while generation_state.stop_condition(population):
        # SELECCION
        # A ambos metodos le doy toda la poblacion, me quedo con A*K de uno y (1-A)*K del otro
        # len(selected_individual_1 + selected_individual_2) = K
        k_selected = Selection.get_both_populations(population, K, A, selection_method_1, selection_method_2)

        # CROSSOVER
        # Obtengo K hijos
        # TODO: ver que hacemos con K impar
        new_people = []
        for i in range(0, len(k_selected), 2):
            new_individual_1, new_individual_2 = Individual.crossover(k_selected[i], k_selected[i+1])
            new_people.append(new_individual_1)
            new_people.append(new_individual_2)

        # MUTACION
        # Muto solo a los hijos (sentido natural)
        new_people = mutation_method(new_people, generations, max_generations)

        # REMPLAZO
        # population = new_people + population
        population = replace_method(population, new_people, population_size, replace_method_1,
                                    replace_method_2, B)

        generations += 1

    max_fitness_individual = None
    max_fitness_value = 0
    min_fitness_individual = None
    min_fitness_value = None
    fitness_sum = 0
    sorted_population = sorted(population, reverse=True)
    ans = []
    # Imprimimos solo los que pide, ordenados por fitness
    for individual in sorted_population[:last_generation_count]:

        ind_fitness = individual.fitness()
        fitness_sum += ind_fitness

        individual_attr = (individual.height(), individual.properties[ItemProp.AGILITY.value], individual.agility(),
                           individual.properties[ItemProp.STRENGTH.value],
                           individual.strength(), individual.properties[ItemProp.RESISTANCE.value],
                           individual.resistance(),
                           individual.properties[ItemProp.EXPERTISE.value], individual.expertise(),
                           individual.properties[ItemProp.LIFE.value], individual.life(),
                           individual_class, crossover, population_0_count, selection_1["name"], selection_2["name"],
                           replace_1["name"], replace_2["name"], replace, mutation, mutation_probability, stop_condition,
                           K, A, B, id)
        ans.append(individual_attr)

        if ind_fitness > max_fitness_value:
            max_fitness_individual = individual
            max_fitness_value = ind_fitness
        if min_fitness_value is None or ind_fitness < min_fitness_value:
            min_fitness_individual = individual
            min_fitness_value = ind_fitness
    return ans
#     TODO: si sirven las otras estadísticas, traerlas aca

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        ans = run_genetic(individual_class=config["class"], crossover=config["crossover"], population_0_count=config["population_0_count"],
                          selection_1=config["selection_1"], selection_2= config["selection_2"], replace_1=config["replace_1"],
                          replace_2=config["replace_2"], replace=config["replace"],
                          mutation=config["mutation"], mutation_probability=config["mutation_probability"],
                          stop_condition=config["stop_condition"], stop_condition_options=config["stop_condition_options"],
                          K=config["K"], A=config["A"], B=config["B"], last_generation_count=config["population_0_count"])

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = config["output"] + "_" + timestamp + ".csv"
        os.makedirs(os.path.dirname(CSV), exist_ok=True)
        file = open(CSV, 'w', newline='')
        writer = csv.writer(file)

        header = ["height", "agility_items", "agility_calculated", "strength_items", "strength_calculated",
                  "resistance_items", "resistance_calculated", "expertise_items", "expertise_calculated", "life_items",
                  "life_calculated",
                  "individual_class", "crossover", "population_0_count", "selection_1", "selection_2",
                  "replace_1", "replace_2", "mutation", "mutation_probability", "stop_condition"
                  "K", "A", "B", "id"]
        writer.writerow(header)
        writer.writerows(ans)

        file.close()

        # TODO: si sirven, ponerlas arriba si queremos, pero no es lo mejor para probar me parece
        # # comparar el fitness con respecto a la poblacion
        # fitness_avg = fitness_sum / population_size
        #
        # # sacar la diversidad genetica del individuo con mas desempeno
        # height_count = 0
        # agility_count = 0
        # strength_count = 0
        # resistance_count = 0
        # expertise_count = 0
        # life_count = 0
        #
        # max_fitness_individual_expertise = max_fitness_individual.expertise()
        # max_fitness_individual_height = max_fitness_individual.height()
        # max_fitness_individual_life = max_fitness_individual.life()
        # max_fitness_individual_resistance = max_fitness_individual.resistance()
        # max_fitness_individual_strength = max_fitness_individual.strength()
        # max_fitness_individual_agility = max_fitness_individual.agility()
        #
        # # TODO: decidir si comparo valores de items o propiedades del character
        #
        # for individual in population:
        #     if individual != max_fitness_individual:
        #         if individual.expertise() >= max_fitness_individual_expertise:
        #             expertise_count += 1
        #         if individual.strength() >= max_fitness_individual_strength:
        #             strength_count += 1
        #         if individual.life() >= max_fitness_individual_life:
        #             life_count += 1
        #         if individual.agility() >= max_fitness_individual_agility:
        #             agility_count += 1
        #         if individual.height() >= max_fitness_individual_height:
        #             height_count += 1
        #         if individual.resistance() >= max_fitness_individual_resistance:
        #             resistance_count += 1
        #
        # # TODO: decidir si quiero buscar otros individuos que tengan EXACTAMENTE los mismos numero o quiero mostrar
        # #  los iguales o mejor
        #
        # # Output a salida estandar
        # print(
        #     f"De nuestra poblacion final, nuestro individuo con mayor fitness presenta un desempeno de {max_fitness_value} y el menor de {min_fitness_value}\n\n")
        # print(f"Nuestro desempeno promedio de la poblacion final tiene un valor de {fitness_avg}\n\n")
        # print(f"Al analizar mas en detalle los datos, podemos observar que\n")
        # print(
        #     f"- Un {height_count / population_size * 100}% de la poblacion es igual o mas alta que el individuo optimo\n")
        # print(
        #     f"- Un {strength_count / population_size * 100}% de la poblacion tiene igual o mas fuerza que el individuo optimo\n")
        # print(
        #     f"- Un {life_count / population_size * 100}% de la poblacion tiene igual o mas vida que el individuo optimo\n")
        # print(
        #     f"- Un {expertise_count / population_size * 100}% de la poblacion tiene igual o mas pericia que el individuo optimo\n")
        # print(
        #     f"- Un {agility_count / population_size * 100}% de la poblacion tiene igual o mas agilidad que el individuo optimo\n")
        # print(
        #     f"- Un {resistance_count / population_size * 100}% de la poblacion tiene igual o mas resistencia que el individuo optimo\n")
