import plotly.graph_objects as go
import pandas as pd
import sys
import csv

def plot_bar_chart(dataframe, type, y_column, y_label, error_bars):
    grouped_data = dataframe.groupby(['Map', 'Algorithm_Heuristic'])
    plot_data = {
        'Mapa': [],
        'Algoritmo': [],
        y_label: [],
    }

    if error_bars:
        plot_data['Top Error Bar'] = []
        plot_data['Bottom Error Bar'] = []

    for (map_value, algorithm), group in grouped_data:
        plot_data['Mapa'].append(map_value.split("/")[-1])
        plot_data['Algoritmo'].append(algorithm)
        mean_value = group[y_column].mean()
        plot_data[y_label].append(mean_value)

        if error_bars:
            plot_data['Top Error Bar'].append(group[y_column].max() - mean_value)
            plot_data['Bottom Error Bar'].append(mean_value - group[y_column].min())

    plot_df = pd.DataFrame(plot_data)
    fig = go.Figure()

    for algorithm in plot_df['Algoritmo'].unique():
        filtered_data = plot_df[plot_df['Algoritmo'] == algorithm]
        error_y_dict = None

        if error_bars:
            error_y_dict = dict(
                type='data',
                symmetric=False,
                array=filtered_data['Top Error Bar'],
                arrayminus=filtered_data['Bottom Error Bar']
            )

        fig.add_trace(go.Bar(
            x=filtered_data['Mapa'],
            y=filtered_data[y_label],
            error_y=error_y_dict,
            name=algorithm
        ))

    fig.update_layout(
        title=f'Comparación entre Algoritmos - {y_label}' if not error_bars else f'Comparación con Barras de Error - {y_label}',
        xaxis_title='Mapa Probado',
        yaxis_title=y_label
    )
    fig.update_yaxes(type='log')
    fig.write_html(f"{sys.argv[1].split('.')[0]}_{type}.html")
    fig.show()

if __name__ == "__main__":
    # Read data from csv
    data = []
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            data.append(row)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=headers)
    df['Execution Time'] = df['Execution Time'].astype(float)
    df['Visited Count'] = pd.to_numeric(df['Visited Count'], errors='coerce')
    df['End State Steps'] = pd.to_numeric(df['End State Steps'], errors='coerce')
    df['Algorithm_Heuristic'] = df.apply(
        lambda row:
            row['Algorithm'] if row['Algorithm'] in ['BFS', 'DFS']
            else f"{row['Algorithm']} ({row['Heuristic']})", axis=1
    )
    plot_bar_chart(df, "visited", "Visited Count", "Cantidad de Nodos Visitados", False)
    plot_bar_chart(df, "time", "Execution Time", "Tiempo de Ejecución (en segundos)", True)
    plot_bar_chart(df, "steps", "End State Steps", "Cantidad de Pasos", False)



