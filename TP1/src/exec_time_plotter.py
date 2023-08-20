# Group the DataFrame by the 'Mapa' and 'Algorithm_Heuristic' fields
grouped_data = df.groupby(['Map', 'Algorithm_Heuristic'])

# Compute the mean, minimum, and maximum 'Execution Time' for each group
plot_data = {
    'Mapa': [],
    'Algoritmo': [],
    'Mean Execution Time': [],
    'Top Error Bar': [],
    'Bottom Error Bar': []
}

for (map_value, algorithm_heuristic), group in grouped_data:
    mean_time = group['Execution Time'].mean()
    min_time = group['Execution Time'].min()
    max_time = group['Execution Time'].max()
    plot_data['Mapa'].append(map_value)
    plot_data['Algoritmo'].append(algorithm_heuristic)
    plot_data['Mean Execution Time'].append(mean_time)
    plot_data['Top Error Bar'].append(max_time - mean_time)
    plot_data['Bottom Error Bar'].append(mean_time - min_time)

plot_df = pd.DataFrame(plot_data)

# Use Plotly to create the scatter plot
import plotly.graph_objects as go

fig = go.Figure()

# Add a trace for each unique algorithm and heuristic pair
for algorithm in plot_df['Algoritmo'].unique():
    filtered_data = plot_df[plot_df['Algoritmo'] == algorithm]
    fig.add_trace(go.Scatter(
        x=filtered_data['Mapa'],
        y=filtered_data['Mean Execution Time'],
        error_y=dict(
            type='data',
            symmetric=False,
            array=filtered_data['Top Error Bar'],
            arrayminus=filtered_data['Bottom Error Bar']
        ),
        name=algorithm
    ))

fig.show()

