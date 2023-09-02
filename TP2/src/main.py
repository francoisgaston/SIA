import sys
import json
from fitness import Fitness
from mutation import MutationEngine
from individual import Individual, ItemProp
from crossover import Crossover
from algorithm import generate_initial_population, select_individuals, replace_individuals, GenerationState
from selection import Selection

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
        selection_method_1 = Selection.get_selection_method(config["selection_1"])
        selection_method_2 = Selection.get_selection_method(config["selection_2"])
        mutation_method = MutationEngine.from_string(config["mutation"])
        K = config["K"]
        A = config["A"]
        B = config["B"]
        # Genero la generacion 0
        population = generate_initial_population(population_size)
        generations = 0

        # primera implementacion que tiene limite de generaciones
        # crear mas implementaciones que permitan otros tipos de corte
        generation_state = GenerationState(config["stop_condition"], sys.argv[2])
        # CONDICION DE CORTE
        # while generations < config["max_generations"]:
        while generation_state.stop_condition():
            # SELECCION
            # A ambos metodos le doy toda la poblacion, me quedo con A*K de uno y (1-A)*K del otro
            # len(selected_individual_1 + selected_individual_2) = K
            selected_individuals_1 = selection_method_1.select(population, int(K * A))
            selected_individuals_2 = selection_method_2.select(population, int(K * (1 - A)))
            k_selected = selected_individuals_1 + selected_individuals_2

            # CROSSOVER
            # Obtengo K hijos
            # TODO: ver que hacemos con K impar
            new_people = []
            for i in range(int(len(k_selected)/2)):
                new_individual_1, new_individual_2 = Individual.crossover(k_selected[i], k_selected[i*2])
                new_people.append(new_individual_1)
                new_people.append(new_individual_2)


            # MUTACION
            # Muto solo a los hijos (sentido natural)
            population_mutation = mutation_method(new_people, generations, config["max_generations"])

            # REMPLAZO
            # unimos a los hijos con los padres
            # TODO: por ahora agarra N del vector, cambiarlo para que funcione con
            population = new_people + population
            population = replace_individuals(population, population_size)


            # --------


            # # RECOMBINACION
            # new_people = []
            # for i in range(int(population_size/2)):
            #     new_individual_1, new_individual_2 = Individual.crossover(population[i], population[i*2])
            #     new_people.append(new_individual_1)
            #     new_people.append(new_individual_2)
            #
            # # MUTACION
            # population_mutation = MutationEngine.from_string(config["mutation"])(population, generations, config["max_generations"])
            # population = population + population_mutation
            #
            # # SELECCION
            # # Agrego los hijos a la generación
            # population = population + new_people
            #
            # # Selecciono los individuos
            # population_1 = random.sample(population, len(population) * A)
            # population_2 = population - population_1
            #
            # selected_individuals_1 = NaturalSelectionEngine.from_string(selection_method_1)(population_1, len(population_1) * A, t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
            # selected_individuals_2 = NaturalSelectionEngine.from_string(selection_method_2)(population_2, len(population_2) * (1-A), t=config["boltzmann"]["t"], m=config["deter_tournament"]["m"])
            # selected_individuals = selected_individuals_1 + selected_individuals_2
            #
            # # REEMPLAZO DE POBLACION
            # population = replace_individuals(selected_individuals, new_people, population_size)

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
        print(f"De nuestra poblacion final, nuestro individuo con mayor fitness presenta un desempeno de {max_fitness_value} y el menor de {min_fitness_value}\n\n")
        print(f"Nuestro desempeno promedio de la poblacion final tiene un valor de {fitness_avg}\n\n")
        print(f"Al analizar mas en detalle los datos, podemos observar que\n")
        print(f"- Un {height_count / population_size * 100}% de la poblacion es igual o mas alta que el individuo optimo\n")
        print(f"- Un {strength_count / population_size * 100}% de la poblacion tiene igual o mas fuerza que el individuo optimo\n")
        print(f"- Un {life_count / population_size * 100}% de la poblacion tiene igual o mas vida que el individuo optimo\n")
        print(f"- Un {expertise_count / population_size * 100}% de la poblacion tiene igual o mas pericia que el individuo optimo\n")
        print(f"- Un {agility_count / population_size * 100}% de la poblacion tiene igual o mas agilidad que el individuo optimo\n")
        print(f"- Un {resistance_count / population_size * 100}% de la poblacion tiene igual o mas resistencia que el individuo optimo\n")
