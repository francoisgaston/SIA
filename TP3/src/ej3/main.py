import os
import datetime  # Import the datetime module
import csv  # Import the csv module
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
    result = np.array_split(result, len(result) / input_length)
    return result

def train_perceptron(config, mlp, data, expected, perceptrons_per_layer):
    i = 0
    if len(data) == 0:
        return []
    min_error = sys.float_info.max
    n = config['n']

    condition = condition_from_str(config['error'], config['epsilon'])
    error = error_from_str(config["error"])
    limit = config["limit"]

    batch = config["batch"] if config["batch"] <= len(data) else len(data)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Specify the folder name
    folder_name = "output"

    # Check if the folder exists. If not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create the filename with the current time and folder
    csv_filename = f"{folder_name}/training_data_{current_time}.csv"

    # Open a new CSV file and create a CSV writer object
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the headers for the CSV file
        csv_writer.writerow(['epoca', 'error_training', 'error_test', 'entrada', 'salida',
                             'capas_ocultas', 'activacion', 'eta', 'beta'])
        
        while not condition.check_stop(min_error) and i < limit:
            final_delta_w = [np.zeros((perceptrons_per_layer[indx], perceptrons_per_layer[indx - 1] + 1)) for indx in
                                  range(len(perceptrons_per_layer)-1, 0 , -1)]
            u_arr = random.sample(range(len(data)), batch)

            for u in u_arr:
                values = mlp.forward(data[u])
                aux_error = np.array(expected[u]) - np.array(values)
                deltas = mlp.backward(aux_error, data[u], n)
                for aux in range(len(final_delta_w)):
                    final_delta_w[aux] += deltas[aux]

            mlp.apply_delta_w(final_delta_w)
            
            # TODO
            error_test = 0
            
            csv_writer.writerow([i, min_error, error_test, config['input'], config['input_length'],
                                 config['perceptrons_for_layers'], config['activation'], config['n'], config['beta']])
            
            new_error = error.compute(data, mlp, expected)
            if condition.check_replace(min_error, new_error):
                print("new error", new_error)
                min_error = new_error

            i += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        expected = np.array(config['expected'])
        data = read_input(config['input'], config['input_length'])
        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])
        mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)
        
        train_perceptron(config, mlp, data, expected, config['perceptrons_for_layers'])

        for weights in mlp.get_all_weights():
            print(weights)

        for i in range(len(data)):
            print("expected: ", expected[i])
            obtained = mlp.forward(data[i])
            print("obtained: ", obtained)

