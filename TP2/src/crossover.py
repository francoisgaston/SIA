from random import randint, random
from individual import Individual
import math

def single_point_crossover(in_1, in_2, lenght):
    num = randint(0, lenght - 1)
    vec1 = in_1[:num] + in_2[num:]
    vec2 = in_2[:num] + in_1[num:]
    return vec1, vec2, num
    # return vec1, vec2


def two_point_crossover(in_1, in_2, lenght):
    num1 = randint(0, lenght - 1)
    num2 = randint(0, lenght - 1)
    max_num = max(num1, num2)
    min_num = min(num1, num2)
    vec1 = in_1[:min_num] + in_2[min_num:max_num] + in_1[max_num:]
    vec2 = in_2[:min_num] + in_1[min_num:max_num] + in_2[max_num:]
    return vec1,vec2,min_num,max_num
    # return vec1, vec2


def uniform_point_crossover(in_1, in_2, lenght):
    vec1 = [0.0] * lenght
    vec2 = [0.0] * lenght
    for i in range(0, lenght):
        if random() >= 0.5:
            vec1[i] = in_1[i]
            vec2[i] = in_2[i]
        else:
            vec1[i] = in_2[i]
            vec2[i] = in_1[i]
    return vec1, vec2


def anular_crossover(in_1, in_2, length):
    # Tomo MAX_PROPS - 1 porque en la teoria todo empieza con indice en 1
    num = randint(0, length - 1)
    len_from = randint(0, math.ceil((length - 1) / 2.0))
    if num + len_from >= length:
        # Hay que volver a empezar
        dif = (num + len_from) % length
        vec1 = in_1[:dif] + in_2[dif:num] + in_1[num:]
        vec2 = in_2[:dif] + in_1[dif:num] + in_2[num:]
        return vec1,vec2,num,len_from
        # return vec1, vec2
    else:
        vec1 = in_1[:num] + in_2[num:num + len_from] + in_1[num + len_from:]
        vec2 = in_2[:num] + in_1[num:num + len_from] + in_2[num + len_from:]
        return vec1, vec2, num, len_from
        # return  vec1, vec2

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

if __name__ == "__main__":
    vec1 = [0.0]*6
    vec2 = [1.0]*6
    max_iter = 5
    len = 6
    print("Single point:")
    for i in range(0, max_iter):
        ans1, ans2, num = single_point_crossover(vec1,vec2,len)
        print(f'Ans are \n{ans1}\n{ans2}\n with num bein {num}')
    print("Two point:")
    for i in range(0, max_iter):
        ans1, ans2, num1, num2 = two_point_crossover(vec1, vec2,len)
        print(f'Ans are \n{ans1}\n{ans2}\n with nums bein {num1} and {num2}')
    print("Uniform point")
    for i in range(0, max_iter):
        ans1, ans2 = uniform_point_crossover(vec1, vec2,len)
        print(f'Ans are \n{ans1}\n{ans2}')
    print("Anular")
    for i in range(0, max_iter):
        ans1, ans2, num, length = anular_crossover(vec1, vec2,len)
        print(f'Ans are \n{ans1}\n{ans2}\n with num bein {num} and len {length}')