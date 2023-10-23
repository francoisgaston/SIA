import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
import json
import sys
import os
import csv
from utils import read_input


def boxplot_graph(headers, scaled_data):
    fig = go.Figure()
    for i in range(len(headers)):
        fig.add_trace(go.Box(y=scaled_data[:, i], name=headers[i]))
    fig.update_layout(title="Variables estandarizadas")
    fig.show()


def component_graph(countries, pc1):
    fig = go.Figure(go.Bar(x=countries, y=pc1))
    fig.update_layout(xaxis_title="País",
                      yaxis_title="PC1",
                      title="PC1 para cada país")
    fig.update_traces(textfont_size=16, textposition='outside', text=pc1, texttemplate='<b>%{text:.2f}</b>')
    fig.show()


def biplot(loadings, PC1, PC2, names, headers):
    fig = px.scatter(x=PC1, y=PC2, text=names, color=PC1, color_continuous_scale='bluered')
    fig.update_traces(textposition='top center', textfont_color='black')

    for i, feature in enumerate(headers):
        fig.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=loadings[i, 0],
            y=loadings[i, 1],
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top",
            arrowcolor="green",
        )
        fig.add_annotation(
            x=loadings[i, 0],
            y=loadings[i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5,
            font=dict(
                color="green",
            )
        )

    fig.update_layout(xaxis_title="PC1",
                      yaxis_title="PC2",
                      title="Valores de las componentes principales 1 y 2",
                      coloraxis_showscale=False)

    fig.show()


def csv_to_compare(names, pc1):
    CSV = f"src/oja/results/pca_vs_oja_bar_PCA.csv"
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "w", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(names)
        csv_writer.writerow(pc1)

def main():
    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        # lectura de input sin nombres de paises
        data, names, headers = read_input(config["input"])

        # Normalizacion de los valores
        scaling = StandardScaler()
        scaling.fit(data)
        Scaled_data = scaling.transform(data)
        boxplot_graph(headers[1::], Scaled_data)

        # Analisis de PCA
        n_components = config["n_components"]
        principal = PCA(n_components)
        principal.fit(Scaled_data)
        x = principal.transform(Scaled_data)

        # TODO: revisar si está bien, creo que si porque es como que estoy eligiendo al primer autovector solo
        pc1 = x[:, 0]

        component_graph(names, pc1)

        # Ordenar los paises segun el valor de la componente principal
        sorted_countries = [country for country in sorted(zip(pc1, names))]
        for idx, country in enumerate(sorted_countries):
            print(f"#{idx + 1} {country[1]}: {country[0].round(2)}")

        if n_components > 1:
            # TODO: Preguntar si esta bien la escala de las flechas (Lo saque de sklearn)
            loadings = principal.components_.T * np.sqrt(principal.explained_variance_)
            pc2 = x[:, 1]
            biplot(loadings, pc1, pc2, names, headers[1::])

        csv_to_compare(names, pc1)


if __name__ == "__main__":
    main()
