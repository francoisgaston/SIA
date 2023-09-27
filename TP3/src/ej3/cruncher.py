
import numpy as np
import sys
import os
import datetime
import csv
import json

from .condition import from_str as condition_from_str
from .activation import from_str as activation_from_str
from .error import from_str as error_from_str
from .multilayerPerceptron import MultiLayerPerceptron
from .main import train_perceptron, read_input, split_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    # Specify the folder name
    folder_name = "./ej3/output"

    # Check if the folder exists. If not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create the filename


    # Open the CSV file and create a CSV writer object

    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)
        csv_filename = f"{folder_name}/{config['output']}_{current_time}.csv"
        print(f'leaving file in ${folder_name}')
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        # Check if the CSV file already exists
        with open(csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the headers for the CSV file only if the file is new
            csv_writer.writerow(['repeticion','epoca', 'error_training', 'error_test', 'entrada', 'salida',
                                     'capas_ocultas', 'activacion', 'eta', 'beta', 'activation', 'error_function',
                                     'batch', 'noise_stddev'])


            expected = np.array(config['expected'])
            data = read_input(config['input'], config['input_length'])  #
            # activation_function = activation_from_str(string=config['activation'], beta=config["beta"])  #
            error = error_from_str(config["error"])
              #
            train_data, train_expected, test_data, test_expected = split_data(data, expected, config["test_pct"])


            def on_min_error(epoch, mlp, min_error):
                print("min_error: ", min_error)


            for activation_function in config["activation"]:
                for beta in config["beta"]:
                    activation_function = activation_from_str(string=activation_function, beta=beta)  #
                    for n in config["n"]:
                        for batch in config["batch"]:
                            for repetition in range(config['repetitions']):
                                def on_epoch(epoch, mlp):
                                    training_error = error.compute(train_data, mlp, train_expected)
                                    test_error = error.compute(test_data, mlp, test_expected)
                                    csv_writer.writerow(
                                        [repetition+1,epoch, training_error, test_error, config['input'],
                                         config['input_length'],
                                         config['perceptrons_for_layers'], activation_function, n,
                                         beta, activation_function, config["error"], batch,
                                         config['noise_stddev']])
                                aux = config.copy()
                                aux["n"] = n
                                aux["batch"] = batch
                                mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)
                                train_perceptron(aux, mlp, train_data, train_expected, on_epoch, on_min_error)

