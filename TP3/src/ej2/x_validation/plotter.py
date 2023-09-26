import sys
import json

import plotly.graph_objects as go
import pandas as pd

from ...activation import from_str as activation_from_str
from .on_epoch import from_str as on_epoch_from_str

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Falta el archivo de resultados CSV y el archivo de configuración utilizado")
        sys.exit(1)

    with open(f"{sys.argv[1]}", "r") as csv_file, open(f"{sys.argv[2]}", "r") as config_file:
        csv = pd.read_csv(csv_file)
        config = json.load(config_file)
        activation = activation_from_str(config["activation"], config["beta"])
        on_epoch = on_epoch_from_str(config["x_validation"]["on_epoch"], activation)
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
            title=f"{on_epoch.name} de entrenamiento y de testeo con {config['x_validation']['k_fold']}-fold cross validation"
                  f"<br><sup>Función de activación: {config['activation']}, con η = {config['eta']} y β = {config['beta']}</sup>",
            xaxis=dict(title="Época"),
            yaxis=dict(title=f"{on_epoch.label}"),
            legend_title="Tipo de error",
        )
        fig.update_yaxes(
            type="log",
        )
        fig.show()
