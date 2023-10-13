import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

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


def biplot(principal, x, names, headers):
    loadings = principal.components_.T * np.sqrt(principal.explained_variance_)
    fig = px.scatter(x, x=0, y=1, text=names)

    for i, feature in enumerate(headers[1::]):
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
            yshift=5,
        )
    fig.show()



def main():
    # lectura de input sin nombres de paises
    data,names, headers = read_input("data/europe.csv")

    # Normalizacion de los valores
    scaling = StandardScaler()
    scaling.fit(data)
    Scaled_data = scaling.transform(data)

    # Analisis de PCA
    principal = PCA(n_components=2)
    principal.fit(Scaled_data)
    x = principal.transform(Scaled_data)

    # TODO: revisar si está bien, creo que si porque es como que estoy eligiendo al primer autovector solo
    pc1 = x[:, 0]
    component_graph(names, pc1)

    biplot(principal, x, names, headers)


if __name__ == "__main__":
    main()