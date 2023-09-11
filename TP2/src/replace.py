from selection import Selection


def traditional_replace(population,  new_population, replaced_population_size, method_1, method_2, B):
    # unir las dos poblaciones
    replaced_population = population + new_population

    # Seleccionamos entre la poblacion actual y la poblacion nueva N individuos
    return Selection.get_both_populations(replaced_population, replaced_population_size, B, method_1, method_2)


def sesgo_replace(population, new_population, replaced_population_size, method_1, method_2, B):
    
    replaced_population = []
    dif = replaced_population_size - len(new_population)
    
    if dif > 0:
        # Si N > K, la nueva poblacion va a estar conformado por los K nuevos individuos y los N-K 
        # restantes son seleccionados entre los individuos de la poblacion actual
        replaced_population += new_population
        replaced_population += Selection.get_both_populations(population, dif, B, method_1, method_2)
    elif dif < 0:
        # Si N < K, la nueva poblacion se va a seleccionar entre los K nuevos individuos
        replaced_population = Selection.get_both_populations(new_population, replaced_population_size, B, method_1, method_2)
    else:
        # Si N = K, retorna K
        replaced_population = new_population
    return replaced_population
    

class Replace:
    @staticmethod
    def from_string(string):
        match string.upper():
            case "TRADICIONAL":
                return traditional_replace
            case "SESGO":
                return sesgo_replace
            case _:
                return

