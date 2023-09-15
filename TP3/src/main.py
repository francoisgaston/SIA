import csv
import random
import pandas as pd

import numpy as np
import json
import sys
import os
import time
from datetime import datetime


# Crea los
def initialize_w(dim=3, start_random=0, stop_random=1):
    ans = []
    for i in range(dim):
        ans.append(random.randrange(start_random, stop_random))
    return ans


# kwargs:
# start_random: inicio para la determinación de los valores iniciales - Double
# stop_random: fin para la determinación de los valores iniciales - Double
# limit: Cantidad máxima de iteraciones del algoritmo - Integer
# initial_error: Valor inicial del error - Double
# p: la cantidad de datos - Integer
# data: es una lista de listas, data[i] es el i-esimo dato y
#       data[i][j] es el valor de su j-esima variable.
#       En la primera columna de cada dato debe haber un 1 - [[Double]]
# expected: Es una lista de los valores esperados, expected[i] es el
#           valor esperado para el i-esimo dato, data[i] - [double]
# stop_condition: Función que determina la condición de corte - (Double) -> Boolean
# compute_error: Función que calcula el error - ([Double], [[Double]]) -> Double
# compute_activation: Función que calcula la activación - ([Double]) -> Double
# compute_delta: Función que calcula la diferencia que toma el vector w
#                   - (Double, Double, [Double], [Double]) -> [Double]
# check_min_error:
def run_perceptron(**kwargs):
    i = 0
    if len(kwargs['data']) == 0:
        return []
    data = kwargs['data']
    expected = kwargs['expected']
    w = np.array(initialize_w(dim=len(data[0]), start_random=kwargs['start_random'], stop_random=kwargs['stop_random']))
    min_error = kwargs['initial_error']
    w_min = None
    # Auxiliar functions
    stop_condition = kwargs['stop_condition']
    compute_error = kwargs['compute_error']
    compute_activation = kwargs['compute_activation']
    compute_delta = kwargs['compute_delta']
    check_min_error = kwargs['check_min_error']

    ans = []

    while stop_condition(min_error) and i < kwargs['limit']:
        u = random.randint(0, len(data) - 1)
        h_u = np.dot(data[u][:len(data[u])], w)
        output_u = compute_activation(h_u)
        delta_w = compute_delta(expected[u], output_u, data[u], w)
        w += delta_w
        error = compute_error(w, data)
        if check_min_error(error, min_error):
            min_error = error
            # Si queremos que se muestre todo el recorrido y no los mejores, poner esto afuera del if
            ans.append(np.copy(w))
            w_min = w
        i += 1

    return ans

if __name__ == "__main__":

    data = []
    expected = []
    dim = 3
    with open("data.csv", 'r', newline='') as data_file:
        #, open("config.json", 'r') as config_file):
        df = pd.read_csv(data_file)



        for _, row in df.iterrows():
            auxdata = []
            x = row['x1']
            dim = len(row) - 1 # -1 porque tenemos el expected
            for i in range(1, dim+1):
                auxdata.append(row["x" + str(i)])
            data.append([1] + auxdata)
            expected.append(row["expected"])


        ans = run_perceptron()

        headers = ["Id"]
        for i in range(len(ans[0])):
            headers.append("w" + str(i))

        # config = json.load(config_file)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # CSV = config["output"] + "_" + timestamp + ".csv"
        CSV = "output_" + timestamp + ".csv"
        os.makedirs(os.path.dirname(CSV), exist_ok=True)
        with open(CSV, "w", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(headers)
            i = 0
            for i in range(len(ans)):
                np.insert(ans[i], 0, i)
                i += 1
            csv_writer.writerows(ans)
            output_file.close()
        data_file.close()
        # config_file.close()
