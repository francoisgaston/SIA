import csv
import pandas as pd
import sys
import plotly.graph_objects as go

# Read the CSV file
data = []
with open(f"{sys.argv[1]}", "r") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    for row in reader:
        data.append(row)

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=headers)
df['Execution Time'] = df['Execution Time'].astype(float)
df['Visited Count'] = pd.to_numeric(df['Visited Count'], errors='coerce')
df['End State Steps'] = pd.to_numeric(df['End State Steps'], errors='coerce')

# Modify the algorithm column to combine algorithm and heuristic if needed
df['Algorithm_Heuristic'] = df.apply(lambda row: row['Algorithm'] if row['Algorithm'] in ['BFS', 'DFS']
                                      else f"{row['Algorithm']} ({row['Heuristic']})", axis=1)

df = df.sort_values(by='Steps')

# Function to plot the graph
def plot_graph(y_column, y_label, error_bars=False):
    # Group by Mapa and Algoritmo
    grouped_data = df.groupby(['Map', 'Algorithm_Heuristic'])
    plot_data = {
        'Mapa': [],
        'Algoritmo': [],
        y_label: [],
    }

    # Add error bar fields if required
    if error_bars:
        plot_data['Top Error Bar'] = []
        plot_data['Bottom Error Bar'] = []

    # Compute the mean, minimum, and maximum for each group
    for (map_value, algorithm), group in grouped_data:
        plot_data['Mapa'].append(map_value.split("/")[-1])
        plot_data['Algoritmo'].append(algorithm)
        mean_value = group[y_column].mean()
        plot_data[y_label].append(mean_value)

        if error_bars:
            plot_data['Top Error Bar'].append(group[y_column].max() - mean_value)
            plot_data['Bottom Error Bar'].append(mean_value - group[y_column].min())

    plot_df = pd.DataFrame(plot_data)

    # Create the scatter plot
    fig = go.Figure()

    # Add a trace for each unique algorithm
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

    # Add labels and title
    title_text = f'Comparación entre Algoritmos - {y_label}' if not error_bars else f'Comparación con Barras de Error - {y_label}'
    fig.update_layout(
        title=title_text,
        xaxis_title='Mapa Probado',
        yaxis_title=y_label
    )

    fig.update_yaxes(type='log', title_text=y_label)

    fig.show()

# Plot graph for Execution Time with error bars
plot_graph('Execution Time', 'Tiempo de Ejecución (segundos)', error_bars=True)

# Plot graph for Visited Count (Nodes Expanded)
plot_graph('Visited Count', 'Nodos Expandidos')

# Plot graph for End State Steps (Optimal Solution Steps)
plot_graph('End State Steps', 'Pasos de la Solución Óptima')

