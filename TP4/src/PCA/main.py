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

def biplot(x, ldngs, names, headers):
    plt.figure(figsize=(8, 8))
    plt.scatter(x[:, 0], x[:, 1])

    for i, feature in enumerate(headers):
        plt.arrow(0, 0, ldngs[0, i], ldngs[1, i], color='r', alpha=0.5)
        plt.text(ldngs[0, i] * 1.15,
                 ldngs[1, i] * 1.15,
                 feature, fontsize=18)

    for i in range(len(names)-1):
        plt.text(x[i, 0], x[i, 1], f'{names[i]}')

    plt.show()

def biplot_plotly(x):
    biplot_df = pd.DataFrame(x, columns=['CP1', 'CP2'])
    fig = px.scatter(biplot_df, x='CP1', y='CP2')

    # Agrega las flechas de las cargas
    for i in range(L.shape[1]):
        fig.add_trace(
            px.scatter(x=[0], y=[0], text=[f'Variable {i + 1}'], name=f'Variable {i + 1}').data[0]
        )
        fig.add_shape(
            x0=0, y0=0, x1=L[0, i], y1=L[1, i],
            line=dict(color='red', width=2, dash='dot'),
            xref='x', yref='y'
        )


def main():
    # lectura de input sin nombres de paises
    data,names, headers = read_input("data/europe.csv")
    print(len(data))
    print(headers)
    print(headers[1::])
    # Normalizacion de los valores
    scaling = StandardScaler()
    scaling.fit(data)
    Scaled_data = scaling.transform(data)
    print(Scaled_data)

    # Analisis de PCA
    principal = PCA(n_components=2)
    principal.fit(Scaled_data)
    x = principal.transform(Scaled_data)
    print(x)

    print("---------")
    print(sum(principal.explained_variance_ratio_))

    # TODO: revisar si está bien, creo que si porque es como que estoy eligiendo al primer autovector solo
    pc1 = x[:, 0]
    component_graph(names, pc1)
    print(len(names))
    print(names[0])
    print(len(pc1))
    print(len(x))
    print("---------")

    loadings = principal.components_.T * np.sqrt(principal.explained_variance_)
    print(len(names.tolist()))
    print(len(x))
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

if __name__ == "__main__":
    main()