import random


def traditional_replace(population,  new_population,  replaced_population_size):
    # El remplazo es igual para ambos
    population += new_population
    replaced_population = []

    # correccion por si len(population) < replace_population_size
    # podria ser un if pero puede ser mas del doble
    while len(replaced_population) + len(population) < replaced_population_size:
        replaced_population += population
    
    replaced_population += random.sample(population, replaced_population_size - len(replaced_population))
    return replaced_population



def sesgo_replace(population, new_population,  replaced_population_size):
    replaced_population = []

    if len(new_population) > replaced_population_size:
        replaced_population = random.sample(new_population, replaced_population_size)
    else:
        replaced_population = new_population
        replaced_population += random.sample(population, replaced_population_size - len(new_population))
    
    return replaced_population


def brecha_replace(population, new_population,  replaced_population_size, g):
    replaced_population = []

    # correccion por si len(new_population) < g * replaced_population_size
    while len(replaced_population) + len(new_population) < g * replaced_population_size:
        replaced_population += new_population

    replaced_population = random.sample(new_population, int(g * replaced_population_size - len(replaced_population)))

    # correccion por si len(population) < (1 - g) * replaced_population_size
    while len(replaced_population) + len(population) < replaced_population_size:
        replaced_population += population
    
    replaced_population += random.sample(population, replaced_population_size - len(replaced_population))

    return replaced_population

    

class Replace:
    @staticmethod
    def from_string(string):
        match string.upper():
            case "TRADICIONAL":
                return traditional_replace_wrapper
            case "SESGO":
                return sesgo_replace_wrapper
            case "BRECHA":
                return brecha_replace
            case _:
                return


# TODO "bien"
# Me basé en la implementacion de selection
def traditional_replace_wrapper(population,  new_population,  replaced_population_size, g):
    return traditional_replace(population,  new_population,  replaced_population_size)

def sesgo_replace_wrapper(population,  new_population,  replaced_population_size, g):
    return sesgo_replace(population,  new_population,  replaced_population_size)

