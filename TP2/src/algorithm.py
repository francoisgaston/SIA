import time
import json
from individual import Individual, ItemProp
from enum import Enum
import random


def read_config(config_file_path):
    with open(f"{config_file_path}", "r") as file:
        config = json.load(file)
        return config["max_generations"], config["max_time"], config["acceptable_solution"], config["limit_generations"]


class GenerationState:

    def __init__(self, method, options):
        self.check_condition = self.condition_from_string(method)

        self.max_gen, _max_time, self.target_fitness, self.limit_generations, self.structure_ratio = options["max_generations"], options["max_time"], options["acceptable_solution"], options["limit_generations"], options["structure_ratio"]
        self.target_time = time.time() + _max_time
        self.current_gen = 0
        self.max_fitness = 0
        self.repeated_generations = 0

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

    def stop_condition(self, population, old_population):
        return self.check_condition(population, old_population)

    def max_generations(self, population, old_population):
        if self.current_gen >= self.max_gen:
            return False
        self.current_gen += 1
        return True

    def max_time(self, population, old_population):
        if time.time() >= self.target_time:
            return False
        return True

    def acceptable_solution(self, population, old_population):
        for individual in population:
            if individual.fitness() >= self.target_fitness:
                return False
        return True

    def check_structure(self, population, old_population):
        
        union_set = set(population).union(old_population)

        difference_ratio = 2 - (len(union_set) / len(population))

        print("     Ratio de diferencia -> " + str(difference_ratio) + " vs " + str(self.structure_ratio))
        # print("union -> " + str(len(union_set)))
        # print("pop -> " + str(len(population)))

        if difference_ratio >= self.structure_ratio:
            self.repeated_generations += 1
            if self.repeated_generations >= self.limit_generations:
                return False
        else:
            self.repeated_generations = 0
        return True

    def check_content(self, population, old_population):
        for individual in population:
            if individual.fitness() > self.max_fitness:
                self.max_fitness = individual.fitness()
                self.repeated_generations = 0
                return True

        if self.repeated_generations > self.limit_generations:
            return False
        
        self.repeated_generations += 1
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
