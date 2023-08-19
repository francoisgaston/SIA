import csv
import plotly.express as px
import pandas as pd

# Read the CSV file
data = []
with open('results.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    for row in reader:
        data.append(row)

# Convert the data to a DataFrame
df = pd.DataFrame(data, columns=headers)
df['Execution Time'] = df['Execution Time'].astype(float) # Convert Execution Time to float
df['Visited Count'] = pd.to_numeric(df['Visited Count'], errors='coerce') # Convert Visited Count to numeric
df['End State Steps'] = pd.to_numeric(df['End State Steps'], errors='coerce') # Convert End State Steps to numeric

# Function to plot the graph
def plot_graph(y_column, y_label):
    # Create a new DataFrame to hold the restructured data
    plot_data = {
        'Mapa': [],
        'Algoritmo': [],
        y_label: []
    }

    # Restructure the data to create the desired plot
    for algorithm in df['Algorithm'].unique():
        filtered_data = df[df['Algorithm'] == algorithm]
        for index, row in filtered_data.iterrows():
            plot_data['Mapa'].append(row['Map'])
            plot_data['Algoritmo'].append(row['Algorithm'])
            plot_data[y_label].append(row[y_column])

    plot_df = pd.DataFrame(plot_data)

    # Plot the line graph
    fig = px.bar(plot_df, x='Mapa', y=y_label, color='Algoritmo', title=f'Comparación entre BFS y DFS - {y_label}', labels={y_label: y_label, 'Mapa': 'Mapa Probado'})
    fig.show()

# Plot graph for Execution Time
plot_graph('Execution Time', 'Tiempo de Ejecución (segundos)')

# Plot graph for Visited Count (Nodes Expanded)
plot_graph('Visited Count', 'Nodos Expandidos')

# Plot graph for End State Steps (Optimal Solution Steps)
plot_graph('End State Steps', 'Pasos de la Solución Óptima')

