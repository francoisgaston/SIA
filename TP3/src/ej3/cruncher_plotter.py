import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import json


def generate_graph(ruta_csv, config):
    # Leer el archivo CSV en un DataFrame de Pandas
    df = pd.read_csv(ruta_csv)

    # Obtener IDs de configuración únicos
    grouped_values = df[config['grouped_by']].unique()
    fig = go.Figure()
    for value in grouped_values:
        # Filtrar el DataFrame basado en config_id
        df_filtrado = df[df[config['grouped_by']] == value].groupby("epoca")
        df_filtrado = df_filtrado["error_training"].agg(["min", "max", "mean"]).reset_index()
        # Ordenar por época
        df_filtrado = df_filtrado.sort_values('epoca')
        first = go.Scatter(x=df_filtrado['epoca'], y=df_filtrado['mean'],
                           name=f'promedio para {config["grouped_by"]} = {value}')
        aux = go.Figure([
            first,
            go.Scatter(x=df_filtrado['epoca'], y=df_filtrado['max'],
                       name=f'maximo para {config["grouped_by"]} = {value}',
                       showlegend=False, mode='lines',
                       marker=first.marker.color,
                       line=dict(width=0)),
            go.Scatter(x=df_filtrado['epoca'], y=df_filtrado['min'],
                       name=f'minimo para {config["grouped_by"]} = {value}',
                       showlegend=False,
                       marker=first.marker.color,
                       line=dict(width=0),
                       mode='lines',
                       fill='tonexty',
                       )
        ])
        for trace in aux.data:
            fig.add_trace(trace)

    fila_muestra = df.iloc[0]
    atributos_config = {
        'Capas Ocultas': fila_muestra['capas_ocultas'],
        'Activacion': fila_muestra['activacion'],
        'Eta': fila_muestra['eta'],
        'Beta': fila_muestra['beta'],
        'Función de Error': fila_muestra['error_function'],
        'Batch': fila_muestra['batch'],
        'Repeticiones': config["repeticiones"]
    }

    texto_anotacion = "<br>".join(
        [f"{k}: {v}" for k, v in atributos_config.items() if k.lower() != config['grouped_by']])
    fig.update_layout(yaxis_type="log", xaxis_title="Época",
                      yaxis_title="Error (logarítmico)",
                      title=f"Comparación de evolución de errores en entrenamiento para {config['grouped_by']} ({config['exercise']})",
                      )
    fig.add_annotation(x=0, y=0, xref="paper", yref="paper",
                       text=texto_anotacion,
                       showarrow=False,
                       font=dict(size=10),
                       bordercolor="black",
                       borderwidth=1,
                       borderpad=4,
                       bgcolor="white",
                       opacity=0.8)
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)

    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)
        ruta_csv = sys.argv[2]
        generate_graph(ruta_csv, config)
