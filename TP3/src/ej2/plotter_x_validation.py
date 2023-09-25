import sys
import json

import plotly.graph_objects as go
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Falta el archivo de resultados CSV y el archivo de configuración utilizado")
        sys.exit(1)

    with open(f"{sys.argv[1]}", "r") as csv_file, open(f"{sys.argv[2]}", "r") as config_file:
        csv = pd.read_csv(csv_file)
        config = json.load(config_file)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                name="Error de entrenamiento",
                x=csv["Epoch"],
                y=csv["train_error"],
                mode="lines",
                line=dict(
                    color="blue"
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                name="Error de testeo",
                x=csv["Epoch"],
                y=csv["test_error"],
                mode="lines",
                line=dict(
                    color="red"
                )
            )
        )
        fig.add_trace(
            go.Scatter(
                name="Error final",
                x=[csv["Epoch"].iloc[-1]],
                y=[csv["test_error"].iloc[-1]],
                mode="markers+text",
                text=[f"<b>Error final<br>{round(csv['test_error'].iloc[-1], 4)}</b>"],
                textposition="top center",
                textfont=dict(
                    size=14,
                    color="red"
                ),
                marker=dict(
                    color="red",
                    size=10,
                ),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                name="Error final",
                x=[csv["Epoch"].iloc[-1]],
                y=[csv["train_error"].iloc[-1]],
                mode="markers+text",
                text=[f"<b>Error final<br>{round(csv['train_error'].iloc[-1], 4)}</b>"],
                textposition="bottom center",
                textfont=dict(
                    size=14,
                    color="blue"
                ),
                marker=dict(
                    color="blue",
                    size=10,
                ),
                showlegend=False,
            )
        )
        fig.update_layout(
            title=f"Error de entrenamiento y de testeo para los datos en {config['data'].split('/')[-1].split('.')[0]}"
                  f"<br><sup>Resultados obtenidos con {config['k_fold']}-fold cross validation en {config['limit']} épocas"
                  f"<br>Función de activación: {config['activation']}, con η = {config['eta']} y β = {config['beta']}</sup>",
            xaxis=dict(title="Época"),
            yaxis=dict(title="MSE"),
            legend_title="Tipo de error",
        )
        fig.update_yaxes(
            type="log",
        )
        fig.show()
