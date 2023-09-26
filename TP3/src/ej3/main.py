import csv  
import datetime
import json
import numpy as np
import sys
from condition import from_str as condition_from_str
from activation import from_str as activation_from_str
from error import from_str as error_from_str
from multilayerPerceptron import MultiLayerPerceptron
import random
import os
import numpy as np

# Recibe la data y lo transforma en np's arrays de cada numero
def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else 0) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    return result

def add_gaussian_noise(data, stddev):
    if(stddev == 0): 
        return data
    noise = np.random.normal(0, stddev, data.shape)
    return data + noise

def split_data(data, expected, test_pct):
    # Shuffle and partition data into training and test sets
    indices = list(range(len(data)))
    random.shuffle(indices)
    split_point = int(test_pct * len(data))  # 80% for training, 20% for testing

    train_indices = indices[:split_point]
    test_indices = indices[split_point:]

    train_data = [data[i] for i in train_indices]
    train_expected = [expected[i] for i in train_indices]
    
    test_data = [data[i] for i in test_indices]
    test_expected = [expected[i] for i in test_indices]

    return train_data, train_expected, test_data, test_expected

def train_perceptron(config, mlp, data, expected, perceptrons_per_layer, on_epoch=None, on_min_error=None):
    if len(data) == 0:
        return []

    data = add_gaussian_noise(np.array(data), config['noise_stddev'])

    train_data, train_expected, test_data, test_expected = split_data(data, expected, config["test_pct"])
    i = 0
    min_error = sys.float_info.max
    n = config['n']

    condition = condition_from_str(config['error'], config['epsilon'])
    error = error_from_str(config["error"])
    limit = config["limit"]

    batch = config["batch"] if config["batch"] <= len(train_data) else len(train_data)

    while not condition.check_stop(min_error) and i < limit:
        final_delta_w = [np.zeros((perceptrons_per_layer[indx], perceptrons_per_layer[indx - 1] + 1)) for indx in
                         range(len(perceptrons_per_layer) - 1, 0, -1)]
        u_arr = random.sample(range(len(train_data)), batch)

        for u in u_arr:
            values = mlp.forward(train_data[u])
            aux_error = np.array(train_expected[u]) - np.array(values)
            deltas = mlp.backward(aux_error, train_data[u], n)
            for aux in range(len(final_delta_w)):
                final_delta_w[aux] += deltas[aux]

        mlp.apply_delta_w(final_delta_w)

        new_error = error.compute(train_data, mlp, train_expected)

        # Calculate test error
        test_error = error.compute(test_data, mlp, test_expected)

        if on_epoch is not None:
            on_epoch(i, mlp, new_error, test_error)

        if condition.check_replace(min_error, new_error):
            if on_min_error is not None:
                on_min_error(i, mlp, min_error)
            min_error = new_error

        i += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    # Specify the folder name
    folder_name = "src/ej3/output"

    # Check if the folder exists. If not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create the filename
    csv_filename = f"{folder_name}/training_data_{current_time}.csv"

    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_filename)

    # Open the CSV file and create a CSV writer object
    with open(csv_filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the headers for the CSV file only if the file is new
        if not file_exists:
            csv_writer.writerow(['config_id', 'epoca', 'error_training', 'error_test', 'entrada', 'salida',
                                'capas_ocultas', 'activacion', 'eta', 'beta', 'activation', 'error_function', 'batch', 'noise_stddev'])

        for config_id, config_file_path in enumerate(sys.argv[1:]):
            with open(config_file_path, "r") as config_file:
                config = json.load(config_file)
                
                expected = np.array(config['expected'])
                data = read_input(config['input'], config['input_length'])  # 
                activation_function = activation_from_str(string=config['activation'], beta=config["beta"])  # 
                mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)  # 
                
                def on_epoch(epoch, mlp, training_error, test_error):
                    csv_writer.writerow([config_id, epoch, training_error, test_error, config['input'], config['input_length'],
                                         config['perceptrons_for_layers'], config['activation'], config['n'],
                                         config['beta'], config['activation'], config["error"], config["batch"], config['noise_stddev']])

                def on_min_error(epoch, mlp, min_error):
                    print("min_error: ", min_error)

                train_perceptron(config, mlp, data, expected, config['perceptrons_for_layers'], on_epoch, on_min_error)  # 

            for weights in mlp.get_all_weights():  # 
                print(weights)

            for i in range(len(data)):
                print("expected: ", expected[i])
                obtained = mlp.forward(data[i])  
                print("obtained: ", obtained)

