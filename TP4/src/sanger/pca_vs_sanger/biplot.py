import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import json
import sys

from numpy import ndarray
from ..utils import read_input_normalize


def biplot_graphs(names: ndarray, headers: ndarray, scikit: tuple, sanger: tuple) -> tuple:
    eigenvecs_fig = go.Figure()

    for i, feature in enumerate(headers):
        eigenvecs_fig.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=scikit[0][i, 0],
            y=scikit[0][i, 1],
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top",
            arrowcolor="lightblue",
        )
        eigenvecs_fig.add_annotation(
            x=scikit[0][i, 0],
            y=scikit[0][i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5,
            font=dict(
                color="lightblue",
            )
        )
        eigenvecs_fig.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=sanger[0][i, 0],
            y=sanger[0][i, 1],
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top",
            arrowcolor="pink",
        )
        eigenvecs_fig.add_annotation(
            x=sanger[0][i, 0],
            y=sanger[0][i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5,
            font=dict(
                color="pink",
            )
        )

    eigenvecs_fig.update_layout(xaxis_title="PC1",
                                yaxis_title="PC2",
                                title=f"Autovectores de scikit-learn y Sanger"
                                      f"<br><sub>Comparando los resultados de scikit-learn y Sanger con eta inicial = {sanger[3]}</sub>",
                                coloraxis_showscale=False)

    coordinates_fig = go.Figure()
    coordinates_fig.add_trace(
        go.Scatter(x=scikit[1], y=scikit[2], mode='markers+text', name="scikit-learn",
                   marker=dict(color="blue"), text=names, textposition='top center', textfont=dict(color="blue")))
    coordinates_fig.add_trace(
        go.Scatter(x=sanger[1], y=sanger[2], mode='markers+text', name="Sanger", marker=dict(color="red"),
                   text=names, textposition='top center', textfont=dict(color="red")))
    coordinates_fig.update_layout(legend_title="Implementación",
                                  title=f"Coordenadas de los países en PC1 y PC2"
                                        f"<br><sub>Comparando los resultados de scikit-learn y Sanger con eta inicial = {sanger[3]}</sub>",
                                    xaxis_title="PC1",
                                    yaxis_title="PC2")

    biplot_fig = go.Figure(eigenvecs_fig)
    biplot_fig.add_trace(coordinates_fig.data[0])
    biplot_fig.add_trace(coordinates_fig.data[1])
    biplot_fig.update_layout(
        title=f"Autovectores y coordenadas de los países en PC1 y PC2"
              f"<br><sub>Comparando los resultados de scikit-learn y Sanger con eta inicial = {sanger[3]}</sub>",
        xaxis_title="PC1",
        yaxis_title="PC2",
        legend_title="Implementación",
        coloraxis_showscale=False)
    return eigenvecs_fig, coordinates_fig, biplot_fig


def get_sanger_data(scaled_data: ndarray) -> tuple:
    with open(f"{sys.argv[2]}", "r") as pc1_file, open(f"{sys.argv[3]}", "r") as pc2_file:
        eta = sys.argv[2].split("_")[-1].rsplit(".", 1)[0].split("-")[0]

        pc1_csv = pd.read_csv(pc1_file)
        pc2_csv = pd.read_csv(pc2_file)

        evector1 = pc1_csv.iloc[-1, 2:].to_numpy()
        evector2 = pc2_csv.iloc[-1, 2:].to_numpy()

        loadings = np.array([evector1, evector2]).T
        pcs = np.matmul(scaled_data, loadings)
        pc1 = pcs[:, 0].tolist()
        pc2 = pcs[:, 1].tolist()

        return loadings, pc1, pc2, eta


def get_scikit_data(scaled_data: ndarray, n_components: int) -> tuple:
    principal = PCA(n_components)
    principal.fit(scaled_data)
    loadings = principal.components_.T * np.sqrt(principal.explained_variance_)

    pcs = principal.transform(scaled_data)
    pc1 = pcs[:, 0]
    pc2 = pcs[:, 1]

    return loadings, pc1, pc2


def main():
    if len(sys.argv) != 4:
        print("Se requiere el archivo de configuración y los archivos de PC1 y PC2")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        # lectura de input sin nombres de paises
        data, names, headers = read_input_normalize(config["input"])

        # Normalizacion de los valores
        scaling = StandardScaler()
        scaling.fit(data)
        scaled_data = scaling.transform(data)

        scikit = get_scikit_data(scaled_data, config["n_components"])
        sanger = get_sanger_data(scaled_data)

        eigenvecs_fig, coordinates_fig, biplot_fig = biplot_graphs(names, headers[1::], scikit, sanger)

        eigenvecs_output = f"{config['output']}/eigenvecs_{sanger[3]}.html"
        eigenvecs_fig.write_html(eigenvecs_output)

        coordinates_output = f"{config['output']}/coordinates_{sanger[3]}.html"
        coordinates_fig.write_html(coordinates_output)

        biplot_output = f"{config['output']}/biplot_{sanger[3]}.html"
        biplot_fig.write_html(biplot_output)


if __name__ == "__main__":
    main()
