import plotly.express as px
from kohonen import Kohonen
from Perceptron import Perceptron
import json
import sys
import numpy as np
import pandas as pd


def read_input_pandas(input_file_path):
    df = pd.read_csv(input_file_path, header=None, skiprows=1)
    for column in df.columns:
        if column != 0:
            df[column] = df[column] - df[column].mean()
            df[column] = df[column] / df[column].std()
    aux = df.to_numpy()
    aux = np.delete(aux, 0, axis=1)
    print(aux)
    return aux, len(aux[0])


def normalize_data(data):
    data_normalize = (data - np.mean(data)) / (np.std(data))
    print(data_normalize)
    return data_normalize


def show_results(results, title):
    fig = px.imshow(
        results,
        labels=dict(color="Resultados"), text_auto=True
    )
    fig.update_layout(
        title=title,
        xaxis_title="Datos",
        yaxis_title="Datos",
    )
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        data, dimension = read_input_pandas(config["input"])
        print(data)
        data = normalize_data(data)
        size = config["size"]
        radius = config["radius"]
        eta = config["eta"]
        Perceptron.SIMILARITY = config["similarity"]
        mult_iterations = config["mult_iterations"]
        kohonen = Kohonen(size=size, dimension=dimension, mult_iterations=mult_iterations, data=data)
        kohonen.train(data)
        results = kohonen.get_activations(data)
        u_data = kohonen.get_u_matrix()
        show_results(results, "matriz de agrupacion")
        show_results(u_data, "matriz u")
