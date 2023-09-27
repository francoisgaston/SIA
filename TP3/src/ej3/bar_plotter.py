import pandas as pd
import plotly.graph_objects as go
import sys

def bar_plot(csv_filename):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_filename)

    # Create a column 'perceptrons_for_layers' that combines 'entrada', 'capas_ocultas', and 'salida'
    df['perceptrons_for_layers'] = df['entrada'].astype(str) + '-' + \
                                   df['capas_ocultas'].astype(str) + '-' + \
                                   df['salida'].astype(str)

    # Group the data by 'config_id', 'iteration', and 'perceptrons_for_layers' to find the minimum 'error_training' and 'error_test' for each iteration
    grouped_df = df.groupby(['config_id', 'iteration', 'perceptrons_for_layers']).agg({'error_training': 'min', 'error_test': 'min'}).reset_index()

    # Calculate the mean and standard deviation of the best (minimum) 'error_training' and 'error_test' across iterations for each 'config_id'
    statistics_df = grouped_df.groupby(['config_id', 'perceptrons_for_layers']).agg({'error_training': ['mean', 'std'], 'error_test': ['mean', 'std']}).reset_index()

    # Create the bar plot
    fig = go.Figure()

    for error_type, label in [('error_training', 'Error de Entrenamiento'), ('error_test', 'Error de Prueba')]:
        fig.add_trace(go.Bar(
            x=statistics_df['perceptrons_for_layers'],
            y=statistics_df[(error_type, 'mean')],
            name=label,
            error_y=dict(type='data', array=statistics_df[(error_type, 'std')]),
        ))

    # Add Spanish labels
    fig.update_layout(
        title='Mejor Error de Entrenamiento y Prueba para Cada Configuración',
        xaxis_title='Perceptrones por Capas',
        yaxis_title='Mejor Error Promedio',
        barmode='group'  # this makes bars appear next to each other
    )

    # Show the plot
    fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)

    bar_plot(sys.argv[1])

