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
                selection_1=None, selection_2=None, replace_1=None,
                replace_2=None, replace="SESGO", mutation="MULTI_GEN_UNIFORM", max_generations=10,
                stop_condition="max_generations", stop_condition_options=None,
                mutation_probability=0.5, K=100, A=0.5, B=0.5, last_generation_count=3, id=1, fulldata=False):
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
    generation_state = GenerationState(stop_condition, stop_condition_options)
    # Generacion 0
    population = generate_initial_population(population_size)
    generations = 0
    old_population = []



    propierties_fulldata = []
    while generation_state.stop_condition(population, old_population):

        if fulldata:
            sorted_population = sorted(population, reverse=True)
            for j in range(len(population)):
                aux = []
                aux.append(sorted_population[j].properties[ItemProp.AGILITY.value])
                aux.append(sorted_population[j].properties[ItemProp.STRENGTH.value])
                aux.append(sorted_population[j].properties[ItemProp.RESISTANCE.value])
                aux.append(sorted_population[j].properties[ItemProp.EXPERTISE.value])
                aux.append(sorted_population[j].properties[ItemProp.LIFE.value])
                aux.append(sorted_population[j].height())
                aux.append(sorted_population[j].fitness())
                aux.append(j)
                aux.append(generations)
                aux.append(id)
                propierties_fulldata.append(aux)
        

        
        # SELECCION
        # A ambos metodos le doy toda la poblacion, me quedo con A*K de uno y (1-A)*K del otro
        # len(selected_individual_1 + selected_individual_2) = K
        k_selected = Selection.get_both_populations(population, K, A, selection_method_1, selection_method_2)

        # CROSSOVER
        # Obtengo K hijos
        # TODO: ver que hacemos con K impar
        new_people = []
        for i in range(0, len(k_selected), 2):
            new_individual_1, new_individual_2 = Individual.crossover(k_selected[i], k_selected[i + 1])
            new_people.append(new_individual_1)
            new_people.append(new_individual_2)

        # MUTACION
        # Muto solo a los hijos (sentido natural)
        new_people = mutation_method(new_people, generations, max_generations)

        # CONDICION DE CORTE
        # Mantengo un registro de la poblacion previa para la condicion estructural
        old_population = list(population)

        # REMPLAZO
        # population = new_people + population
        population = replace_method(population, new_people, population_size, replace_method_1,
                                    replace_method_2, B)

        generations += 1
        # print("Generacion -> " + str(generations))

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

        individual_attr = (individual.fitness(), individual.attack(), individual.defense(), individual.height(),
                           individual.properties[ItemProp.AGILITY.value],
                           individual.properties[ItemProp.STRENGTH.value],
                           individual.properties[ItemProp.RESISTANCE.value],
                           individual.properties[ItemProp.EXPERTISE.value],
                           individual.properties[ItemProp.LIFE.value],
                           individual_class, crossover, population_0_count, selection_1["name"], selection_2["name"],
                           replace_1["name"], replace_2["name"], replace, mutation, mutation_probability,
                           stop_condition,
                           K, A, B, id)
        ans.append(individual_attr)

        if ind_fitness > max_fitness_value:
            max_fitness_individual = individual
            max_fitness_value = ind_fitness
        if min_fitness_value is None or ind_fitness < min_fitness_value:
            min_fitness_individual = individual
            min_fitness_value = ind_fitness
    
    if fulldata:
        return ans, propierties_fulldata
    
    return ans


#     TODO: si sirven las otras estadísticas, traerlas aca

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        ans, propierties_fulldata = run_genetic(individual_class=config["class"], crossover=config["crossover"],
                          population_0_count=config["population_0_count"],
                          selection_1=config["selection_1"], selection_2=config["selection_2"],
                          replace_1=config["replace_1"],
                          replace_2=config["replace_2"], replace=config["replace"],
                          mutation=config["mutation"], mutation_probability=config["mutation_probability"],
                          stop_condition=config["stop_condition"],
                          stop_condition_options=config["stop_condition_options"],
                          K=config["K"], A=config["A"], B=config["B"],
                          last_generation_count=config["population_0_count"])

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


        header = ["AGILITY", "STRENGTH", "RESISTANCE", "EXPERTISE", "LIFE", "height",
                  "fitness", "id", "generations",
                  "id_config"]

        writer.writerow(header)
        writer.writerows(propierties_fulldata)

        file.close()

