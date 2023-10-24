import numpy as np
import pandas as pd
from kohonen import Kohonen
from Perceptron import Perceptron
import json
import datetime
import os
import sys
import csv
def read_input_pandas(input_file_path):
    df = pd.read_csv(input_file_path, header=None, skiprows=1)
    for column in df.columns:
        if column != 0:
            aux = df[column] - df[column].mean()
            df[column] = aux / df[column].std()
    aux = df.to_numpy()
    aux = np.delete(aux, 0, axis=1)
    names = pd.read_csv(input_file_path)
    names = names['Country']
    # print(aux)
    return aux, len(aux[0]), names


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        data, dimension, names = read_input_pandas(config["input"])
        ans = []

        for repetition in range(config["repetitions"]):
            for initial_radius in config["initial_radius"]:
                for initial_eta in config["initial_eta"]:
                    for size in config["size"]:
                        for variable_radius in config["variable_radius"]:
                            for variable_eta in config["variable_eta"]:
                                for mult_iterations in config["mult_iterations"]:
                                    for similarity in config["similarity"]:
                                        Perceptron.SIMILARITY = similarity
                                        for data_initialization in config["data_initialization"]:
                                            kohonen = Kohonen(size=size, initial_radius=initial_radius,
                                                              initial_eta=initial_eta,
                                                              variable_radius=variable_radius,
                                                              variable_eta=variable_eta,
                                                              dimension=dimension, mult_iterations=mult_iterations,
                                                              data=data if data_initialization else None)

                                            kohonen.train(data)
                                            results, _ = kohonen.get_activations(data, names)
                                            u_data = kohonen.get_u_matrix()

                                            heatmap_mean = results.mean()
                                            u_matrix_mean = u_data.mean()
                                            ans.append([repetition,initial_radius,initial_eta,size,variable_radius,
                                                        variable_eta,mult_iterations,similarity,data_initialization,
                                                        heatmap_mean,u_matrix_mean])


        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"output/{config['output']}_{current_time}.csv"
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        with open(csv_filename,mode='a', newline='') as out:
            csv_writer = csv.writer(out)

            # Write the headers for the CSV file only if the file is new
            csv_writer.writerow(['repetition', 'initial_radius', 'initial_eta', 'size', 'variable_radius', 'variable_eta',
                                 'mult_iterations', 'similarity', 'data_initialization',"heatmap_mean","u_matrix_mean"])
            csv_writer.writerows(ans)


if __name__ == "__main__":
    main()