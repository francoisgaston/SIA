import plotly.express as px
from kohonen import Kohonen
from Perceptron import Perceptron
import plotly.graph_objects as go
import json
import sys
import numpy as np
import pandas as pd


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

def show_heatmap(results, title, names):
    for i in range(len(names)):
        for j in range(len(names[i])):
            aux = names[i][j]
            grouped_names = [aux[i:i + 3] for i in range(0, len(aux), 3)]
            formatted_cell = '<br> '.join([', '.join(group) for group in grouped_names])
            names[i][j] = formatted_cell

    fig = go.Figure(data = go.Heatmap(
        z=results,
        text=names,
        texttemplate="%{text}",
        textfont={"size": 10}
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Datos",
        yaxis_title="Datos",
    )
    fig.show()

def show_u_matrix(results, title):
    fig = go.Figure(data=go.Heatmap(
        z=results,
        colorscale='gray'
    ))
    fig.update_layout(
        title=title,
    )
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)
        data, dimension, names = read_input_pandas(config["input"])
        # print(data)
        size = config["size"]
        radius = config["radius"]
        eta = config["eta"]
        Perceptron.SIMILARITY = config["similarity"]
        mult_iterations = config["mult_iterations"]
        kohonen = Kohonen(size=size, radius=None, dimension=dimension, mult_iterations=mult_iterations, data=data)
        kohonen.train(data)
        results, activation_names = kohonen.get_activations(data, names)
        u_data = kohonen.get_u_matrix()
        show_heatmap(results, "matriz de agrupacion", activation_names)
        show_u_matrix(u_data, "matriz u")
