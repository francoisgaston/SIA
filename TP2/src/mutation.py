import random

from individual import Individual

class MutationEngine:

    MUTATION_PROBABILITY = 0.5


    @staticmethod
    def _gen_mutation(individuals, mutation_probability):
        mutated_individuals = []
        for individual in individuals:
            if random.random() < mutation_probability:
                mutated_individuals.append(individual.mutate_gen(random.uniform(0, Individual.MAX_PROPS), individual))
            else:
                mutated_individuals.append(individual)

        return mutated_individuals

    @staticmethod
    def gen_uniform_mutation(individuals):
        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY)

    @staticmethod
    def gen_non_uniform_mutation(individuals, generation, max_generations):
        if(generation == None or max_generations == None):
            raise ValueError("wrong values to mutation")

        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY * (1- generation / max_generations))
    
    @staticmethod
    def _multi_gen_mutation(individuals, mutation_probability):
        mutated_individuals = []
        for individual in individuals:
            mutated_individual = individual
            for gene in individual.properties: # encapsulacion modo python
                if random.random() < mutation_probability:
                    mutated_individual = individual.mutate_gen(gene, individual)
            mutated_individuals.append(mutated_individual)

        return mutated_individuals


    @staticmethod
    def multi_gen_uniform_mutation(individuals):
        return MutationEngine._multi_gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY)

    @staticmethod
    def multi_gen_non_uniform_mutation(individuals, generation, max_generations):
        if generation == None or max_generations == None:
            raise ValueError("wrong values to mutation")

        return MutationEngine._multi_gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY * (1 - generation / max_generations))

    @staticmethod
    def from_string(string, generation=None, max_generations=None):
        match string.upper():
            case "GEN_UNIFORM":
                return MutationEngine.gen_uniform_mutation
            case "GEN_NON_UNIFORM":
                return MutationEngine.gen_non_uniform_mutation
            case "MULTI_GEN_UNIFORM":
                return MutationEngine.multi_gen_uniform_mutation
            case "MULTI_GEN_NON_UNIFORM":
                return MutationEngine.multi_gen_non_uniform_mutation
            case _:
                return None
