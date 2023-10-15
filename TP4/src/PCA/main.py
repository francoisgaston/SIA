import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import json
import sys

def read_input(input_file_path):
    df = pd.read_csv(input_file_path)
    headers = df.columns.tolist()
    names = df['Country']
    selected_columns = df.loc[:, df.columns != 'Country']
    selected_columns = selected_columns.iloc[0:]
    aux = selected_columns.to_numpy()
    # aux = np.delete(aux, 0, axis=1)
    return aux, names, headers


def component_graph(countries, pc1):
    fig = go.Figure([go.Bar(x=countries,y=pc1)])
    fig.update_layout(xaxis_title="País",
                      yaxis_title="PC1",
                      title="PC1 para cada país")
    fig.show()


def biplot(loadings, PC1, PC2, names, headers):
    fig = px.scatter(x=PC1, y=PC2, text=names)
    fig.update_traces(textposition='top center')

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
            yanchor="top"
        )
        fig.add_annotation(
            x=loadings[i, 0],
            y=loadings[i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            text=feature,
            yshift=5
        )

    fig.update_layout(xaxis_title="PC1",
                      yaxis_title="PC2",
                      title="Valores de las componentes principales 1 y 2")

    fig.show()



def main():
    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        # lectura de input sin nombres de paises
        data, names, headers = read_input(config["input"])

        # Normalizacion de los valores
        scaling = StandardScaler()
        scaling.fit(data)
        Scaled_data = scaling.transform(data)

        # Analisis de PCA
        n_components = config["n_components"]
        principal = PCA(n_components)
        principal.fit(Scaled_data)
        x = principal.transform(Scaled_data)

        # TODO: revisar si está bien, creo que si porque es como que estoy eligiendo al primer autovector solo
        pc1 = x[:, 0]
        component_graph(names, pc1)

        if n_components>1:
            # TODO: Preguntar si esta bien la escala de las flechas (Lo saque de sklearn)
            loadings = principal.components_.T * np.sqrt(principal.explained_variance_)
            pc2 = x[:, 1]
            biplot(loadings, pc1, pc2, names, headers[1::])


if __name__ == "__main__":
    main()