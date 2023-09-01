import time
import json
from individual import Individual, ItemProp
from enum import Enum


def read_config(config_file_path):
    with open(f"{config_file_path}", "r") as file:
        config = json.load(file)
        return config["max_generations"], config["max_time"]


class GenerationState:

    def __int__(self, method, config_file_path):
        self.check_condition = self.condition_from_string(method)
        self.max_gen, _max_time = read_config(config_file_path)
        self.target_time = time.time() + _max_time
        self.current_gen = 0

    def condition_from_string(self, method):
        match method.upper():
            case "MAX_GENERATIONS":
                return self.max_generations
            case "MAX_TIME":
                return self.max_time
            case "ACCEPTABLE_SOLUTION":
                return self.acceptable_solution
            case "CHECK_STRUCTURE":
                return self.check_structure
            case "CHECK_CONTENT":
                return self.check_content
            case _:
                return self.max_generations

    def stop_condition(self):
        return self.check_condition()

    def max_generations(self):
        if self.current_gen >= self.max_gen:
            return False
        self.current_gen += 1
        return True

    def max_time(self):
        if time.time() >= self.target_time:
            return False
        return True

    def acceptable_solution(self):
        return True

    def check_structure(self):
        return True

    def check_content(self):
        return True




# Creación de la generación inicial
def generate_initial_population(n):
    population = []

    for _ in range(n):
        individual = Individual.generate_individual()
        population.append(individual)

    return population



def select_individuals(population):
    return population


def replace_individuals(population, new_people, population_size):
    return random.sample(population, population_size)





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
