import math
import random
from math import exp
from individual import Individual


class NaturalSelectionEngine:
    # TODO: Definirlo en el archivo de configuracion y setearlo en main
    boltzmann_k = 1
    boltzmann_tc = 0
    boltzmann_t0 = 0

    @staticmethod
    def elite_selection(population, k):
        sorted_population = sorted(population, key=Individual.fitness, reverse=True)
        n = len(sorted_population)
        elite_population = []
        for i, individual in enumerate(sorted_population):
            times = math.ceil((k - i) / n)
            for _ in range(times):
                elite_population.append(Individual.clone(individual))
        return elite_population

    # qi_array MUST be ordered (ascending order)
    @staticmethod
    def roulette(qi_array, rj_array):
        individuals_index = []
        for rj in rj_array:
            for i, qi in enumerate(qi_array):
                if qi > rj:
                    individuals_index.append(i)
                    break
        return individuals_index

    @staticmethod
    def roulette_selection(population, k):
        total_fitness = sum(Individual.fitness(individual) for individual in population)
        selected = []

        qi_accum = 0
        qi_array = []
        for individual in population:
            pi = Individual.fitness(individual) / total_fitness
            qi_accum += pi
            qi_array.append(qi_accum)

        rj_array = []
        for _ in range(k):
            rj_array.append(random.uniform(0.0, 1.0))

        for idx in NaturalSelectionEngine.roulette(qi_array, rj_array):
            selected.append(Individual.clone(population[idx]))
        return selected

    @staticmethod
    def universal_selection(population, k):
        total_fitness = sum(Individual.fitness(individual) for individual in population)
        selected = []

        qi_accum = 0
        qi_array = []
        for individual in population:
            pi = Individual.fitness(individual) / total_fitness
            qi_accum += pi
            qi_array.append(qi_accum)

        rj_array = []
        for j in range(k):
            r = random.uniform(0.0, 1.0)
            rj_array.append((r + j) / k)

        for idx in NaturalSelectionEngine.roulette(qi_array, rj_array):
            selected.append(Individual.clone(population[idx]))
        return selected

    @staticmethod
    def ranking_selection(population, k):
        sorted_population = sorted(population, key=Individual.fitness, reverse=False)
        n = len(sorted_population)

        qi_array = []
        for i, individual in enumerate(sorted_population):
            qi_array.append(i / n)

        # TODO: Usa los rj de ruleta o de universal?
        rj_array = []
        for _ in range(k):
            rj_array.append(random.uniform(0.0, 1.0))

        selected = []
        for idx in NaturalSelectionEngine.roulette(qi_array, rj_array):
            selected.append(Individual.clone(sorted_population[idx]))
        return selected

    @staticmethod
    def boltzmann_selection(population, k, **kwargs):
        # Como e^x es creciente, entonces sirve ordenar la poblacion por su fitness real
        sorted_population = sorted(population, key=Individual.fitness, reverse=False)
        T = NaturalSelectionEngine.boltzmann_tc + (
                    NaturalSelectionEngine.boltzmann_t0 - NaturalSelectionEngine.boltzmann_tc) * exp(-k * kwargs['t'])

        boltzmann_values = [exp(Individual.fitness(ind) / T) for ind in sorted_population]
        avg_boltzmann = sum(boltzmann_values) / len(sorted_population)

        exp_values = [boltzmann_value / avg_boltzmann for boltzmann_value in boltzmann_values]

        # TODO: Usa los rj de ruleta o de universal?
        rj_array = []
        for _ in range(k):
            rj_array.append(random.uniform(0.0, 1.0))

        selected = []
        for idx in NaturalSelectionEngine.roulette(exp_values, rj_array):
            selected.append(Individual.clone(sorted_population[idx]))
        return selected

    @staticmethod
    def deterministic_tournament_selection(population, k, **kwargs):
        selected = []
        for _ in range(k):
            # TODO: Se puede volver a elegir a un individuo si ya se eligio en un paso anterior?
            random_individuals = sorted(random.sample(population, kwargs['m']), key=Individual.fitness, reverse=True)
            selected.append(Individual.clone(random_individuals[0]))
        return selected

    @staticmethod
    def probabilistic_tournament_selection(population, k):
        selected = []
        for _ in range(k):
            # TODO: Se puede volver a elegir a un individuo si ya se eligio en un paso anterior?
            threshold = random.uniform(0.5, 1.0)
            random_pair = sorted(random.sample(population, 2), key=Individual.fitness, reverse=True)
            r = random.uniform(0.0, 1.0)
            if r < threshold:
                selected.append(Individual.clone(random_pair[0]))
            else:
                selected.append(Individual.clone(random_pair[1]))
        return selected

    @staticmethod
    def from_string(string):
        match string.upper():
            case "ELITE":
                return NaturalSelectionEngine.elite_selection
            case "ROULETTE":
                return NaturalSelectionEngine.roulette_selection
            case "UNIVERSAL":
                return NaturalSelectionEngine.universal_selection
            case "RANKING":
                return NaturalSelectionEngine.ranking_selection
            case "BOLTZMANN":
                return NaturalSelectionEngine.boltzmann_selection
            case "DETER_TOURNAMENT":
                return NaturalSelectionEngine.deterministic_tournament_selection
            case "PROBA_TOURNAMENT":
                return NaturalSelectionEngine.probabilistic_tournament_selection
            case _:
                return
