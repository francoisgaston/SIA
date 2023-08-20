import csv
import plotly.express as px
import pandas as pd
import sys

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

# Add a new column to the DataFrame that combines the Algorithm and Heuristic
df['Algorithm_Heuristic'] = df['Algorithm'] + df['Heuristic'].apply(lambda x: '' if x == 'NONE' else ' - ' + x)

color_mapping = {algorithm: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] 
                 for i, algorithm in enumerate(df['Algorithm_Heuristic'].unique())}

# Function to plot the graph
def plot_graph(y_column, y_label):
    # Create a new DataFrame to hold the restructured data
    plot_data = {
        'Mapa': [],
        'Algoritmo': [],
        y_label: []
    }

    # Restructure the data to create the desired plot
    for algorithm in df['Algorithm_Heuristic'].unique():
        filtered_data = df[df['Algorithm_Heuristic'] == algorithm]
        for index, row in filtered_data.iterrows():
            plot_data['Mapa'].append(row['Map'])
            plot_data['Algoritmo'].append(row['Algorithm_Heuristic'])
            plot_data[y_label].append(row[y_column])

    plot_df = pd.DataFrame(plot_data)

    fig = px.line(plot_df, x='Mapa', y=y_label, color='Algoritmo', title=f'Comparación entre Algoritmos - {y_label}', 
                  labels={y_label: y_label, 'Mapa': 'Mapa Probado'},
                  color_discrete_map=color_mapping) # Use the color mapping here
    fig.show()

# Plot graph for Execution Time
plot_graph('Execution Time', 'Tiempo de Ejecución (segundos)')

# Plot graph for Visited Count (Nodes Expanded)
plot_graph('Visited Count', 'Nodos Expandidos')

# Plot graph for End State Steps (Optimal Solution Steps)
plot_graph('End State Steps', 'Pasos de la Solución Óptima')

