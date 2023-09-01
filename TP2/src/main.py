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
        # configuraciones
        config = json.load(file)
        Individual.FITNESS_FUNCTION = Fitness.from_string(config["class"])
        Individual.CROSSOVER_FUNCTION = Crossover.from_string(config["crossover"])
        population_size = config["population_0_count"]
        selection_method_1 = config["selection_1"]
        selection_method_2 = config["selection_2"]
        A = config["A"]

        # Genero la generacion 0
        population = generate_initial_population(population_size)
        generations = 0

        # primera implementacion que tiene limite de generaciones
        # crear mas implementaciones que permitan otros tipos de corte
        if config["stop_condition"] == "max_generations":
            # generation_state = GenerationState(config["stop_condition"], sys.argv[2])
            # CONDICION DE CORTE
            while generations < config["max_generations"]:
            # while generation_state.stop_condition():

                # RECOMBINACION
                new_people = []
                for i in range(population_size/2):
                    new_people.append = Crossover.from_string(config["crossover"])(population[i], population[i*2])

                # MUTACION
                population_mutation = MutationEngine.from_string(config["mutation"])(population, generations, config["max_generations"])
                population = population + population_mutation

                # SELECCION
                # Agrego los hijos a la generación
                population = population + new_people

                # Selecciono los individuos
                population_1 = random.sample(population, len(population) * A)
                population_2 = population - population_1

                selected_individuals_1 = NaturalSelectionEngine.from_string(selection_method_1)(population_1, len(population_1) * A, t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
                selected_individuals_2 = NaturalSelectionEngine.from_string(selection_method_2)(population_2, len(population_2) * (1-A), t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
                selected_individuals = selected_individuals_1 + selected_individuals_2
            
                # REEMPLAZO DE POBLACION
                population = replace_individuals(selected_individuals, new_people, population_size)

                generations += 1

