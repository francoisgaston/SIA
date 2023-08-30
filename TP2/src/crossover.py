from random import randint, random
from individual import Individual
import math

def single_point_crossover(individual_1, individual_2):
    num = randint(0, Individual.MAX_PROPS - 1)
    vec1 = individual_1.properties[:num] + individual_2.properties[num:]
    vec2 = individual_1.properties[num:] + individual_2.properties[:num]
    return vec1, vec2


def two_point_crossover(individual_1, individual_2):
    num1 = randint(0, Individual.MAX_PROPS - 1)
    num2 = randint(0, Individual.MAX_PROPS - 1)
    max_num = max(num1, num2)
    min_num = min(num1, num2)
    vec1 = individual_1.properties[:min_num] + individual_2.properties[min_num:max_num] + individual_1.properties[
                                                                                          max_num:]
    vec2 = individual_2.properties[:min_num] + individual_1.properties[min_num:max_num] + individual_2.properties[
                                                                                          max_num:]
    return vec1, vec2


def uniform_point_crossover(individual_1, individual_2):
    vec1 = [0.0] * Individual.MAX_PROPS
    vec2 = [0.0] * Individual.MAX_PROPS
    for i in range(0, Individual.MAX_PROPS):
        if random() >= 0.5:
            vec1[i] = individual_1.properties[i]
            vec2[i] = individual_2.properties[i]
        else:
            vec1[i] = individual_2.properties[i]
            vec2[i] = individual_1.properties[i]
    return vec1, vec2


# TODO: revisar
def anular_crossover(individual_1, individual_2):
    # Tomo MAX_PROPS - 1 porque en la teoria todo empieza con indice en 1
    num = randint(0, Individual.MAX_PROPS - 1)
    len = randint(0, math.ceil((Individual.MAX_PROPS-1)/2.0))
    if num + len >= Individual.MAX_PROPS:
        # Hay que volver a empezar
        dif = Individual.MAX_PROPS - (num + len)
        vec1 = individual_1.properties[:dif] + individual_2.properties[dif:num] + individual_1.properties[num:]
        vec2 = individual_2.properties[:dif] + individual_1.properties[dif:num] + individual_2.properties[num:]
        return vec1, vec2
    else:
        vec1 = individual_1.properties[:num] + individual_2.properties[num:num+len] + individual_1.properties[num+len:]
        vec2 = individual_2.properties[:num] + individual_1.properties[num:num+len] + individual_2.properties[num+len:]
        return  vec1, vec2

class Crossover:
    @staticmethod
    def from_string(string):
        match string.upper():
            case "SINGLE_POINT":
                return single_point_crossover
            case "TWO_POINT":
                return two_point_crossover
            case "UNIFORM_POINT":
                return uniform_point_crossover
            case "ANULAR":
                return anular_crossover
            case _:
                return
