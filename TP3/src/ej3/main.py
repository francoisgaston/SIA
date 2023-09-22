import json
import numpy as np
import sys
from condition import from_str as condition_from_str
from activation import from_str as activation_from_str
from error import from_str as error_from_str
from multilayerPerceptron import MultiLayerPerceptron
import random


# Recibe la data y lo transforma en np's arrays de cada numero
def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else 0) for character in file1.read().split()]
    # result = list(map(mapper, file1.read().split()))
    result = np.array_split(result, len(result) / input_length)
    return result


# config:
# limit: Cantidad máxima de iteraciones del algoritmo - Integer
# expected: Es una lista de los valores esperados, expected[i] es el
#           valor esperado para el i-esimo dato, results[i] - [[Integer]]
# condition: Clase con funciones para determinar el corte y cómo comparar valores
#     check_stop(self, curr_error) -> Boolean - determina si se debe terminar el algoritmo en base al error
#     check_replace(self, curr_error, new_error) -> Boolean - determina si se debe cambiar
#       el valor de curr_error por new_error
# error: Clase con función que calcula el error -
#   compute(self, results, expected, w) -> Double
# activation: Clase con funciones que calcula la activación
#   eval(self, x) -> Double - evalúa la función de activación para un valor x
#   diff(self, x) -> Double - evalúa la derivada de la función de activación para un valor x
# n: tasa de aprendizaje
def train_perceptron(config, mlp, data, expected):
    i = 0
    if len(data) == 0:
        return []
    min_error = sys.float_info.max
    n = config['n']
    # Auxiliar functions
    condition = condition_from_str(config['error'], config['epsilon'])
    error = error_from_str("QUADRATIC_MULTILAYER")
    limit = config["limit"]

    while not condition.check_stop(min_error) and i < limit:
        # TODO: hacer el batch 
        u = random.randint(0, len(data) - 1)

        # Valoes de las neuronas de salida
        values = mlp.forward(data[u])

        # expected = [0] * len(expected)
        # expected[u] = 1
        aux_error = np.array(expected[u]) - np.array(values)

        mlp.backward(aux_error, data[u], n)

        new_error = error.compute(data, mlp, expected)

        if condition.check_replace(min_error, new_error):
            print("new error", new_error)
            min_error = new_error

        i += 1


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        expected = np.array(config['expected'])

        data = read_input(config['input'], config['input_length'])
        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])

        mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)

        train_perceptron(config, mlp, data, expected)

        for i in range(len(data)):
            print("expected: ", expected[i])
            obtained = mlp.forward(data[i])
            print("obtained: ", obtained)


