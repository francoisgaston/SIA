
from src.individual import Individual, ItemProp


# Creación de la generación inicial
def generate_initial_population(n):
    population = []

    for _ in range(n):
        individual = Individual.generate_individual()
        population.append(individual)

    return population



def select_individuals(population):
    return population


def replace_individuals(population, new_people):
    return population



def stop_condition():
    return True


'''
def genetic_algorithm():
    population_0 = []
    population = []

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        generations = 0
        population_0 = generate_initial_population(config["population_0_count"])

        # primera implementacion que tiene limite de generaciones
        # crear mas implementaciones que permitan otros tipos de corte
        if config["stop_condition"] == "max_generations":
            while generations < config["max_generations"] and final_condition():
                selected = select_individuals(population)

                # aplicar cruce y mutacion
                new_people = Crossover.crossover(population[0], population[1])

                population = replace_individuals(population, new_people)
                generations += 1
                

# Creación de la generación inicial
def generate_initial_population(n):
    population = []

    for _ in range(n):
        strength, agility, expertise, resistance, life = generate_random_items()
        height = set_height()
        individual = Individual(strength, agility, expertise, resistance, life, height)
        population.append(individual)

    return population
'''
