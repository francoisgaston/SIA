import json
import sys
import numpy as np

from ..main import read_input, split_data, train_perceptron
from ..activation import from_str as activation_from_str
from ..multilayerPerceptron import MultiLayerPerceptron
from ..utils.write_csv import create_csv, append_row_to_csv


# Ejecutar desde TP3: pipenv run python -m src.ej3.metric.confusion_matrix src/ej3/configs/config_digits_logistic.json

def calculate_confusion_matrix(mlp, data, expected, precision):
    dim = len(expected[0])
    matrix = np.zeros((dim, dim))
    undecided = np.zeros(dim)

    for i in range(len(data)):
        result = mlp.forward(data[i])
        correct_index = np.argmax(expected[i])
        result_index = np.argmax(result)
        if correct_index == result_index:
            # print(result[correct_index], expected[i][correct_index])
            # Si el resultado es correcto y tiene un error de precision menor a la tolerada, se considera correcto
            if abs(result[correct_index] - expected[i][correct_index]) <= precision:
                matrix[correct_index][correct_index] += 1
            # Si el resultado es correcto pero tiene un error de precision mayor a la tolerada, se considera incorrecto (falso negativo)
            else:
                undecided[correct_index] += 1
        else:
            matrix[correct_index][result_index] += 1

    # print(matrix)

    # Para una clase i, los verdaderos positivos se encuentran en la posicion i,i de la matriz
    results = [{"tp": matrix[i][i], "tn": 0, "fp": 0, "fn": undecided[i]} for i in range(dim)]
    for i in range(dim):
        # Para una clase i, los falsos negativos son la suma de la fila i sin la diagonal
        results[i]["fn"] += np.sum(matrix[i]) - matrix[i][i]
        # Para una clase i, los verdaderos positivos son la suma de la columna i sin la diagonal
        results[i]["fp"] += np.sum(matrix[:, i]) - matrix[i][i]
        # Para una clase i, los verdaderos negativos son la suma de todos los elementos de la matriz
        # menos los de la fila i y la columna i
        results[i]["tn"] += np.sum(matrix) - results[i]["tp"] - results[i]["fp"] - results[i]["fn"]

    return results


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)

        expected = np.array(config['expected'])
        data = read_input(config['input'], config['input_length'])
        train_data, train_expected, test_data, test_expected = split_data(data, expected, config["test_pct"])

        precision = config["metric"]["precision"]
        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])

        mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)

        headers = ["epoch", "tp", "tn", "fp", "fn"]
        filename = config["output"] + config['input'].split("/")[-1].split(".")[0]
        training_filename = create_csv(filename + "_train", headers)
        test_filename = create_csv(filename + "_test", headers)

        def on_epoch(epoch, mlp):
            print("Calculando la matriz de confusion para la época ", epoch)
            print("Calculando la matriz de confusion para el conjunto de entrenamiento")
            training_results = calculate_confusion_matrix(mlp, train_data, train_expected, precision)
            for i in range(len(training_results)):
                row = [epoch, training_results[i]["tp"], training_results[i]["tn"], training_results[i]["fp"],
                       training_results[i]["fn"]]
                append_row_to_csv(training_filename, row)
            print("Calculando la matriz de confusion para el conjunto de testeo")
            test_results = calculate_confusion_matrix(mlp, test_data, test_expected, precision)
            for i in range(len(test_results)):
                row = [epoch, test_results[i]["tp"], test_results[i]["tn"], test_results[i]["fp"],
                       test_results[i]["fn"]]
                append_row_to_csv(test_filename, row)


        train_perceptron(config, mlp, train_data, train_expected, on_epoch)
