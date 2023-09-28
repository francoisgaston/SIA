import json
import sys
import numpy as np
import plotly.express as px
from ..main import read_input, split_data, train_perceptron
from ..activation import from_str as activation_from_str
from ..multilayerPerceptron import MultiLayerPerceptron
from ..utils.write_csv import create_csv, append_row_to_csv


# Ejecutar desde TP3: pipenv run python -m src.ej3.metric.confusion_matrix src/ej3/configs/config_digits_logistic.json

def add_gaussian_noise(data, labels, stddev):
    if stddev == 0:
        return data, labels
    noisy_data = np.absolute(data + np.random.normal(0, stddev, data.shape))
    noisy_labels = labels.copy()
    return noisy_data, noisy_labels


def augment_training_data(data, labels, noise_stddev):
    noisy_data, noisy_labels = add_gaussian_noise(np.array(data), np.array(labels), noise_stddev)
    return np.concatenate((data, noisy_data)), np.concatenate((labels, noisy_labels))


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
    results = [{"tp": matrix[i][i], "tn": 0, "fp": 0, "fn": 0} for i in range(dim)]
    for i in range(dim):
        # Para una clase i, los falsos negativos son la suma de la fila i sin la diagonal
        results[i]["fn"] += np.sum(matrix[i]) - matrix[i][i]
        # Para una clase i, los falsos positivos son la suma de la columna i sin la diagonal
        results[i]["fp"] += np.sum(matrix[:, i]) - matrix[i][i]
        # Para una clase i, los verdaderos negativos son la suma de todos los elementos de la matriz
        # menos los de la fila i y la columna i
        results[i]["tn"] += np.sum(matrix) - results[i]["tp"] - results[i]["fp"] - results[i]["fn"]

    return results, matrix


ans = [1]

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)

        expected = np.array(config['expected'])
        data = read_input(config['input'], config['input_length'])
        # Data augmentation
        for i in range(2):
            data, expected = augment_training_data(data, expected, config['stddev'])
        train_data, train_expected, test_data, test_expected = split_data(data, expected, config["test_pct"])

        precision = config["metric"]["precision"]
        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])

        mlp = MultiLayerPerceptron(config['perceptrons_for_layers'], activation_function)

        headers = ["epoch", "tp", "tn", "fp", "fn"]
        filename = config["output"] + config['input'].split("/")[-1].split(".")[0]
        training_filename = create_csv(filename + "_train", headers)
        test_filename = create_csv(filename + "_test", headers)

        def on_epoch(epoch, mlp, _):
            print("Calculando la matriz de confusion para la época ", epoch)
            print("Calculando la matriz de confusion para el conjunto de entrenamiento")
            training_results, _ = calculate_confusion_matrix(mlp, train_data, train_expected, precision)
            for i in range(len(training_results)):
                row = [epoch, training_results[i]["tp"], training_results[i]["tn"], training_results[i]["fp"],
                       training_results[i]["fn"]]
                append_row_to_csv(training_filename, row)
            print("Calculando la matriz de confusion para el conjunto de testeo")
            test_results, _ = calculate_confusion_matrix(mlp, test_data, test_expected, precision)
            for i in range(len(test_results)):
                row = [epoch, test_results[i]["tp"], test_results[i]["tn"], test_results[i]["fp"],
                       test_results[i]["fn"]]
                append_row_to_csv(test_filename, row)

        train_perceptron(config, mlp, train_data, train_expected, on_epoch)
        training_results, training_matrix = calculate_confusion_matrix(mlp, train_data, train_expected, precision)
        test_results, test_matrix = calculate_confusion_matrix(mlp, test_data, test_expected, precision)

        fig = px.imshow(
            training_matrix,
            labels=dict(color="Resultados"), text_auto=True
        )
        fig.update_layout(
            title=f"Matriz de confusion para el conjunto de entrenamiento"
                  f"<br><sup>Tamaño del conjunto: {len(train_data)}</sup>",
            xaxis_title="Prediccion",
            yaxis_title="Real",
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                ticktext=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                ticktext=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            )
        )
        fig.show()

        fig = px.imshow(
            test_matrix,
            labels=dict(color="Resultados"), text_auto=True
        )
        fig.update_layout(
            title=f"Matriz de confusion para el conjunto de testeo"
                  f"<br><sup>Tamaño del conjunto: {len(test_data)}</sup>",
            xaxis_title="Prediccion",
            yaxis_title="Real",
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                ticktext=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                ticktext=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            )
        )
        fig.show()
