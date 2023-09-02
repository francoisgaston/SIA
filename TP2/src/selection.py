import math
import random
from math import exp
from individual import Individual
from abc import ABC, abstractmethod


class Roulette:
    @staticmethod
    def get_roulette_qi_array(population):
        total_fitness = sum(individual.fitness() for individual in population)
        qi_accum = 0
        qi_array = []
        for individual in population:
            pi = individual.fitness() / total_fitness
            qi_accum += pi
            qi_array.append(qi_accum)
        return qi_array

    @staticmethod
    def get_roulette_rj_array(k):
        rj_array = []
        for _ in range(k):
            rj_array.append(random.uniform(0.0, 1.0))
        return rj_array

    # qi_array MUST be ordered (ascending order)
    @staticmethod
    def roulette(population, qi_array, rj_array):
        if len(qi_array) != len(population):
            raise Exception("qi_array and population must have the same length")
        individuals = []
        for rj in rj_array:
            for i, qi in enumerate(qi_array):
                if qi > rj:
                    individuals.append(Individual.clone(population[i]))
                    break
        return individuals


class Selection(ABC):
    @abstractmethod
    def select(self, population, k):
        pass

    @staticmethod
    def get_selection_method(selection_data):
        if "name" not in selection_data:
            raise Exception("Selection method name not found")
        match selection_data["name"].upper():
            case "ELITE":
                return EliteSelection()
            case "ROULETTE":
                return RouletteSelection()
            case "UNIVERSAL":
                return UniversalSelection()
            case "RANKING":
                return RankingSelection()
            case "BOLTZMANN":
                if "tc" not in selection_data or "t0" not in selection_data or "c" not in selection_data:
                    raise Exception("Boltzmann selection method needs tc, t0 and c parameters")
                return BoltzmannSelection(selection_data["tc"], selection_data["t0"], selection_data["c"])
            case "DETER_TOURNAMENT":
                if "m" not in selection_data:
                    raise Exception("Deterministic tournament selection method needs m parameter")
                return DeterministicTournamentSelection(selection_data["m"])
            case "PROBA_TOURNAMENT":
                return ProbabilisticTournamentSelection()
            case _:
                raise Exception("Selection method not found")


class EliteSelection(Selection):
    def select(self, population, k):
        sorted_population = sorted(population, reverse=True)
        n = len(sorted_population)
        elite_population = []
        for i, individual in enumerate(sorted_population):
            times = math.ceil((k - i) / n)
            for _ in range(times):
                elite_population.append(Individual.clone(individual))
        return elite_population


class RouletteSelection(Selection):
    def select(self, population, k):
        return Roulette.roulette(population, Roulette.get_roulette_qi_array(population), Roulette.get_roulette_rj_array(k))


class UniversalSelection(Selection):
    def select(self, population, k):
        rj_array = []
        r = random.uniform(0.0, 1.0)
        for j in range(k):
            rj_array.append((r + j) / k)

        return Roulette.roulette(population, Roulette.get_roulette_qi_array(population), rj_array)


class RankingSelection(Selection):
    def select(self, population, k):
        sorted_population = sorted(population, reverse=False)
        n = len(sorted_population)

        qi_array = []
        for i, individual in enumerate(sorted_population):
            qi_array.append(i / n)

        return Roulette.roulette(sorted_population, qi_array, Roulette.get_roulette_rj_array(k))


class BoltzmannSelection(Selection):
    def __init__(self, tc, t0, c):
        self.tc = tc
        self.t0 = t0
        self.c = c
        self.t = 0

    def select(self, population, k):
        # Como e^x es creciente, entonces sirve ordenar la poblacion por su fitness real
        sorted_population = sorted(population, reverse=False)
        T = self.tc + (self.t0 - self.tc) * exp(-self.c * self.t)

        boltzmann_values = [exp(individual.fitness() / T) for individual in sorted_population]
        avg_boltzmann = sum(boltzmann_values) / len(sorted_population)

        exp_values = [boltzmann_value / avg_boltzmann for boltzmann_value in boltzmann_values]
        self.t += 1

        return Roulette.roulette(sorted_population, exp_values, Roulette.get_roulette_rj_array(k))


class DeterministicTournamentSelection(Selection):
    def __init__(self, m):
        self.m = m

    def select(self, population, k):
        selected = []
        for _ in range(k):
            random_individuals = sorted(random.sample(population, self.m), reverse=True)
            selected_individual = random_individuals[0]
            # Filtramos para que no se repitan los individuos
            # Es decir, actualizamos la poblacion a considerar para la proxima iteracion de seleccion
            # removiendo al individuo seleccionado
            population = list(filter(lambda ind: ind != selected_individual, population))
            selected.append(selected_individual)
        return selected


class ProbabilisticTournamentSelection(Selection):
    def select(self, population, k):
        selected = []
        for _ in range(k):
            threshold = random.uniform(0.5, 1.0)
            random_pair = sorted(random.sample(population, 2), reverse=True)
            r = random.uniform(0.0, 1.0)
            selected_individual = None
            if r < threshold:
                selected_individual = random_pair[0]
            else:
                selected_individual = random_pair[1]
            # Filtramos para que no se repitan los individuos
            # Es decir, actualizamos la poblacion a considerar para la proxima iteracion de seleccion
            # removiendo al individuo seleccionado
            population = list(filter(lambda ind: ind != selected_individual, population))
            selected.append(selected_individual)
        return selected
