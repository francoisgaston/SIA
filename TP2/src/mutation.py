import random

from individual import Individual

class MutationEngine:

    MUTATION_PROBABILITY = 0.5


    @staticmethod
    def _gen_mutation(individuals, mutation_probability):
        mutated_individuals = []
        for individual in individuals:
            if random.random() < MutationEngine.MUTATION_PROBABILITY:
                mutated_individuals.append(individual.mutate_gen(random.uniform(0, Individual.MAX_PROPS)))
            else:
                mutated_individuals.append(individual)

        return mutated_individuals

    @staticmethod
    def gen_uniform_mutation(individuals):
        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY)

    @staticmethod
    def gen_non_uniform_mutation(individuals, generation, max_generations):
        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY * (1- generation / max_generations))
    
    @staticmethod
    def _multi_gen_mutation(individuals, mutation_probability):
        mutated_individuals = []
        for individual in individuals:
            mutated_individual = individual
            for gene in individual.properties: # encapsulacion modo python
                if random.random() < mutation_probability:
                    mutated_individual = individual.mutate_gen(gene)
            mutated_individuals.append(mutated_individual)

        return mutated_individuals


    @staticmethod
    def multi_gen_uniform_mutation(individuals):
        return MutationEngine._multi_gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY)

    @staticmethod
    def multi_gen_non_uniform_mutation(individuals, generation, max_generations):
        return MutationEngine._multi_gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY * (1 - generation / max_generations))

    @staticmethod
    def from_string(string, generation=None, max_generations=None):
        match string.upper():
            case "GEN_UNIFORM":
                return lambda individuals: MutationEngine.gen_uniform_mutation(individuals)
            case "GEN_NON_UNIFORM":
                return lambda individuals: MutationEngine.gen_non_uniform_mutation(individuals, generation, max_generations)
            case "MULTI_GEN_UNIFORM":
                return lambda individuals: MutationEngine.multi_gen_uniform_mutation(individuals)
            case "MULTI_GEN_NON_UNIFORM":
                return lambda individuals: MutationEngine.multi_gen_non_uniform_mutation(individuals, generation, max_generations)
            case _:
                return None
