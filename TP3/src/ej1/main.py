import random
import pandas as pd
import numpy as np
import json
import sys

from ..error import from_str as error_from_str
from ..condition import from_str as condition_from_str
from ..activation import from_str as activation_from_str
from ..utils.write_csv import write_csv

# Correr el script desde TP3: pipenv run python -m src.ej1.main src\ej1\config\config.json

# Crea los valores iniciales para cada w_i
def initialize_w(dim=3, start_random=0, stop_random=1):
    ans = []
    for i in range(dim):
        ans.append(random.uniform(start_random, stop_random))
    return ans


# kwargs:
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
# n: tasa de aprendizaje?
def run_perceptron(**kwargs):
    i = 0
    if len(kwargs['data']) == 0:
        return []
    data = kwargs['data']
    expected = kwargs['expected']
    w = np.array(initialize_w(dim=len(data[0]), start_random=kwargs['start_random'], stop_random=kwargs['stop_random']))
    min_error = sys.float_info.max
    n = kwargs['n']
    w_min = None
    # Auxiliar functions
    condition = kwargs['condition']
    error = kwargs['error']
    activation = kwargs['activation']

    ans = [w.tolist()]

    while not condition.check_stop(min_error) and i < kwargs['limit']:
        u = random.randint(0, len(data) - 1)
        h_u = np.dot(data[u], w)
        output_u = activation.eval(h_u)
        # delta_w = compute_delta(expected[u], output_u, results[u], w)
        # TODO: creo que esta es una forma genérica de hacerlo
        delta_w = n * (expected[u] - output_u) * activation.diff(h_u) * data[u]
        w += delta_w
        new_error = error.compute(data, expected, w)
        if condition.check_replace(min_error, new_error):
            min_error = new_error
            print("min_error", min_error)
            # Si queremos que se muestre todo el recorrido y no los mejores, poner esto afuera del if
            w_min = w
        ans.append(w.tolist())
        i += 1

    return ans, w_min


if __name__ == "__main__":
    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        data = []
        expected = []
        with open(config['data'], 'r', newline='') as data_file:
            df = pd.read_csv(data_file)

            for _, row in df.iterrows():
                auxdata = []
                dim = len(row) - 1  # -1 porque tenemos el expected
                for i in range(1, dim + 1):
                    auxdata.append(row["x" + str(i)])
                data.append(np.array([1] + auxdata))
                expected.append(row["y"])

        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])
        # Si no es lineal, escalamos los datos de entrada
        activation_function.scale(expected)
        ans, last = run_perceptron(
            start_random=config['random_interval'][0],
            stop_random=config['random_interval'][1],
            limit=config['iteration_limit'],
            data=data,
            expected=expected,
            condition=condition_from_str(config['error'], config['epsilon']),
            error=error_from_str(config['error'], activation_function=activation_function),
            activation=activation_function,
            n=config['eta']
        )

        filename = 'results/' + config['output'] + config['data'].split("/")[-1].split(".")[0]
        headers = ["Id"]
        for i in range(len(ans[0])):
            headers.append("w" + str(i))
        for i in range(len(ans)):
            # Los np.arrays son inmutables
            ans[i] = np.insert(ans[i], 0, i)
        write_csv(filename, headers, ans)