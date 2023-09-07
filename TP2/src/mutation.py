from random import randint, random

from individual import Individual

class MutationEngine:

    MUTATION_PROBABILITY = None


    @staticmethod
    def _gen_mutation(individuals, mutation_probability):
        for individual in individuals:
            if random() < mutation_probability:
                individual.mutate_gen(randint(0, Individual.MAX_PROPS-1))
        #     Normalizar
            individual.normalize()
        return individuals

    @staticmethod
    def gen_uniform_mutation(individuals, generation, max_generations):
        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY)

    @staticmethod
    def gen_non_uniform_mutation(individuals, generation, max_generations):
        if(generation == None or max_generations == None):
            raise ValueError("wrong values to mutation")

        return MutationEngine._gen_mutation(individuals, MutationEngine.MUTATION_PROBABILITY * (1- generation / max_generations))
    
    @staticmethod
    def _multi_gen_mutation(individuals, mutation_probability):
        for individual in individuals:
            for gene in range(0, Individual.MAX_PROPS):
                if random() < mutation_probability:
                    individual.mutate_gen(gene)
            individual.normalize()
        return individuals


    @staticmethod
    def multi_gen_uniform_mutation(individuals, generation, max_generations):
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
