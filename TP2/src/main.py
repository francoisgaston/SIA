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
                new_people = MutationEngine.from_string(config["mutation"])(new_people, generations,
                                                                            config["max_generations"])

                # SELECCION
                selected_individuals_1 = NaturalSelectionEngine.from_string(selection_method_1)(population,
                                                                                                population_size * A,
                                                                                                t=config["boltzmann"][
                                                                                                    "t"], m=config[
                        "deter_tournament"]["m"])
                selected_individuals_2 = NaturalSelectionEngine.from_string(selection_method_2)(population,
                                                                                                population_size * (
                                                                                                        1 - A),
                                                                                                t=config["boltzmann"][
                                                                                                    "t"], m=config[
                        "deter_tournament"]["m"])
                selected_individuals = selected_individuals_1 + selected_individuals_2

                # REEMPLAZO DE POBLACION
                population = replace_individuals(population, new_people)

                generations += 1

        # else other conditions

        # encuentro el individuo con mejor desempeno
        max_fitness_individual = None
        max_fitness_value = 0
        min_fitness_individual = None
        min_fitness_value = None
        fitness_sum = 0
        for individual in population:
            ind_fitness = individual.fitness()
            fitness_sum += ind_fitness
            if ind_fitness > max_fitness_value:
                max_fitness_individual = individual
                max_fitness_value = ind_fitness
            if min_fitness_value is None or ind_fitness < min_fitness_value:
                min_fitness_individual = individual
                min_fitness_value = ind_fitness

        # comparar el fitness con respecto a la poblacion
        fitness_avg = fitness_sum / population_size

        # sacar la diversidad genetica del individuo con mas desempeno
        height_count = 0
        agility_count = 0
        strength_count = 0
        resistance_count = 0
        expertise_count = 0
        life_count = 0

        max_fitness_individual_expertise = max_fitness_individual.expertise()
        max_fitness_individual_height = max_fitness_individual.height()
        max_fitness_individual_life = max_fitness_individual.life()
        max_fitness_individual_resistance = max_fitness_individual.resistance()
        max_fitness_individual_strength = max_fitness_individual.strength()
        max_fitness_individual_agility = max_fitness_individual.agility()

        for individual in population:
            if individual != max_fitness_individual:
                if individual.expertise() >= max_fitness_individual_expertise:
                    expertise_count += 1
                if individual.strength() >= max_fitness_individual_strength:
                    strength_count += 1
                if individual.life() >= max_fitness_individual_life:
                    life_count += 1
                if individual.agility() >= max_fitness_individual_agility:
                    agility_count += 1
                if individual.height() >= max_fitness_individual_height:
                    height_count += 1
                if individual.resistance() >= max_fitness_individual_resistance:
                    resistance_count += 1

        # Output a salida estandar
        print("De nuestra poblacion final, nuestro individuo con mayor fitness presenta un desempeno de %f y el menor "
              "de %f\n\n", max_fitness_value, min_fitness_value)
        print("Nuestro desempeno promedio de la poblacion final tiene un valor de %f\n", fitness_avg)
        print("Al analizar mas en detalle los datos, podemos observar que\n")
        print("- Un %f% de la poblacion es igual o mas alta que el individuo optimo",
              height_count / population_size * 100)
        print("- Un %f% de la poblacion tiene igual o mas fuerza que el individuo optimo",
              strength_count / population_size * 100)
        print("- Un %f% de la poblacion tiene igual o mas vida que el individuo optimo",
              life_count / population_size * 100)
        print("- Un %f% de la poblacion tiene igual o mas pericia que el individuo optimo",
              expertise_count / population_size * 100)
        print("- Un %f% de la poblacion tiene igual o mas agilidad que el individuo optimo",
              agility_count / population_size * 100)
        print("- Un %f% de la poblacion tiene igual o mas resistencia que el individuo optimo",
              resistance_count / population_size * 100)
