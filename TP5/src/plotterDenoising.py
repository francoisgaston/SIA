import plotly.graph_objects as go
import pandas as pd
import datetime

def plot_line_chart(data_frames, tags):
    # Create a figure
    fig = go.Figure()

    # Iterate through each DataFrame in the array
    for df_idx, df in enumerate(data_frames):
        # Extract the 'Epoch' and 'Value' columns
        epoch_values = df[['Epoch', 'Value']].values

        # Extract the 'Epoch' and 'Value' values
        epochs = epoch_values[:, 0]
        values = epoch_values[:, 1]

        # Add a line trace for each DataFrame
        fig.add_trace(go.Scatter(x=epochs, y=values, mode='lines', name=f'{tags[df_idx]}'))

    # Customize the layout
    fig.update_layout(
        title='Variacion de la maxima diferencia de bits',
        xaxis_title='Epoch',
        yaxis_title='Maxima diferencia de bits',
        legend_title='Configuraciones',
    )

    # Show the figure
    fig.show()
