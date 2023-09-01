class MutationEngine:
    @staticmethod
    def gen_uniform_mutation(individuals):
        mutated_individuals = []
        return mutated_individuals

    @staticmethod
    def gen_non_uniform_mutation(individuals):
        mutated_individuals = []
        return mutated_individuals

    @staticmethod
    def multi_gen_uniform_mutation(individuals):
        mutated_individuals = []
        return mutated_individuals

    @staticmethod
    def multi_gen_non_uniform_mutation(individuals):
        mutated_individuals = []
        return mutated_individuals

    def from_string(string):
        match string.upper():
            case "GEN_UNIFORM":
                return lambda individuals: MutationEngine.gen_uniform_mutation(individuals)
            case "GEN_NON_UNIFORM":
                return lambda individuals: MutationEngine.gen_non_uniform_mutation(individuals)
            case "MULTI_GEN_UNIFORM":
                return lambda individuals: MutationEngine.multi_gen_uniform_mutation(individuals)
            case "MULTI_GEN_NON_UNIFORM":
                return lambda individuals: MutationEngine.multi_gen_non_uniform_mutation(individuals)
            case _:
                return None
