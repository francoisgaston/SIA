import json
import numpy as np

import sys 
# config:
# start_random: inicio para la determinación de los valores iniciales - Double
# stop_random: fin para la determinación de los valores iniciales - Double
# limit: Cantidad máxima de iteraciones del algoritmo - Integer
# initial_error: Valor inicial del error - Double
# results: es una lista de listas, results[i] es el i-esimo dato (debe ser una np.array) y
#       results[i][j] es el valor de su j-esima variable.
#       En la primera columna de cada dato debe haber un 1 - [[Double]]
# expected: Es una lista de los valores esperados, expected[i] es el
#           valor esperado para el i-esimo dato, results[i] - [double]
# condition: Clase con funciones para determinar el corte y cómo comparar valores
#     check_stop(self, curr_error) -> Boolean - determina si se debe terminar el algoritmo en base al error
#     check_replace(self, curr_error, new_error) -> Boolean - determina si se debe cambiar
#       el valor de curr_error por new_error
# error: Clase con función que calcula el error -
#   compute(self, results, expected, w) -> Double
# activation: Clase con funciones que calcula la activación
#   eval(self, x) -> Double - evalúa la función de activación para un valor x
#   diff(self, x) -> Double - evalúa la derivada de la función de activación para un valor x
# n: tasa de aprendizaje? TODO: preguntar
def train_perceptron(config, mlp, data, expected):
    i = 0
    if len(data) == 0:
        return []
    min_error = sys.float_info.max
    n = config['n']
    # Auxiliar functions
    condition = condition_from_str(config['error'], config['epsilon'])
    error = error_from_str(config['error'], activation_function=activation_function)
    activation = kwargs['activation']
    

# Recibe la data y lo transforma en np's arrays de cada numero
def read_input(file, input_lenght):
    file1 = open(file,"r+")
    result = file1.read().split()
    result = np.array_split(result, len(result)/input_lenght)
    return results



if __name__ == "__main__":

    data = read_input(config['input'], config['input_lenght'])

    # Dividimos la entrada en 35 valores
    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.read

    # metemos esa entrada en un perceptron
    mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)
    error = error_from_str(config['error'], activation_function=activation_function)
    limit = config['iteration_limit']
    condition=condition_from_str(config['error'], config['epsilon'])
    
    train_perceptron()
     
     


    #joche va a la uade


    