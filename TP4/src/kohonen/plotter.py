import pandas as pd
import plotly.graph_objects as go
import sys
import json


def generate_graph(ruta_csv, config):
    # Leer el archivo CSV en un DataFrame de Pandas
    df = pd.read_csv(ruta_csv)

    grouped_df = df.groupby(config['group_by']).agg(u_mean=("u_matrix_mean",'mean'),u_max=('u_matrix_mean','max'),u_min=("u_matrix_mean",'min'),heatmap_mean=('heatmap_mean',max)).reset_index()
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=grouped_df[config['group_by']], y=grouped_df['u_mean'], error_y=dict(type='data',
            symmetric=False,
            array=grouped_df['u_max'],
            arrayminus=grouped_df['u_min']),name="u_matrix_mean"))
    fig.add_trace(go.Scatter(x=grouped_df[config['group_by']], y=grouped_df['heatmap_mean'],name="heatmap_mean"))
    fig.update_layout(title=config["title"],
    xaxis=dict(title=config['group_by']))
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)

    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)
        ruta_csv = sys.argv[2]
        generate_graph(ruta_csv, config)
