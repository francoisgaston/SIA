import sys
import json
from fitness import Fitness
from mutation import MutationEngine
from individual import Individual
from crossover import Crossover
from algorithm import generate_initial_population, select_individuals, replace_individuals
from src.selection_engine import NaturalSelectionEngine

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        Individual.FITNESS_FUNCTION = Fitness.from_string(config["class"])
        Individual.CROSSOVER_FUNCTION = Crossover.from_string(config["crossover"])
        population_size = config["population_0_count"]
        population = generate_initial_population(population_size)
        selection_method_1 = config["selection_1"]
        selection_method_2 = config["selection_2"]
        A = config["A"]

        generations = 0

        # primera implementacion que tiene limite de generaciones
        # crear mas implementaciones que permitan otros tipos de corte
        if config["stop_condition"] == "max_generations":
            # generation_state = GenerationState(config["stop_condition"], sys.argv[2])
            # CONDICION DE CORTE
            while generations < config["max_generations"]:
            # while generation_state.stop_condition():

                # RECOMBINACION
                new_people = Crossover.from_string(config["crossover"])(selected[1], selected[0])

                # MUTACION
                new_people = MutationEngine.from_string(config["mutation"])(new_people)

                # SELECCION
                selected_individuals_1 = NaturalSelectionEngine.from_string(selection_method_1)(population, population_size * A, t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
                selected_individuals_2 = NaturalSelectionEngine.from_string(selection_method_2)(population, population_size * (1-A), t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
                selected_individuals = selected_individuals_1 + selected_individuals_2
            
                # REEMPLAZO DE POBLACION
                population = replace_individuals(population, new_people)

                generations += 1

