import pandas as pd
import plotly.graph_objects as go
import sys

def bar_plot(csv_filename):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_filename)

    # Create a column 'perceptrons_for_layers' that combines 'entrada', 'capas_ocultas', and 'salida'
    df['perceptrons_for_layers'] = df['capas_ocultas'].astype(str) + ', noise:' + df['noise_stddev'].astype(str) + ', augmeted:' + df['data_augmentation'].astype(str)


    # Create a unique configuration identifier based on the three fields
    df['unique_config_id'] = df['noise_stddev'].astype(str) + "_" + df['capas_ocultas'].astype(str) + "_" + df['data_augmentation'].astype(str)

    # Compute the mean and standard deviation for each unique 'unique_config_id'
    statistics_df = df.groupby(['unique_config_id', 'perceptrons_for_layers']).agg({'error_training': ['mean', 'std'], 'error_test': ['mean', 'std']}).reset_index()

    # Sort by the length of 'perceptrons_for_layers'
    statistics_df['sort_key'] = statistics_df['perceptrons_for_layers'].apply(len)
    statistics_df = statistics_df.sort_values('sort_key').reset_index(drop=True)

    # Create the bar plot
    fig = go.Figure()

    for error_type, label in [('error_training', 'Error de Entrenamiento'), ('error_test', 'Error de Prueba')]:
        mean_values = statistics_df[(error_type, 'mean')].values
        std_values = statistics_df[(error_type, 'std')].values

        # Ensure the error bars don't go below zero
        lower_error = mean_values - std_values
        lower_error[lower_error < 0] = 0

        fig.add_trace(go.Bar(
            x=statistics_df['perceptrons_for_layers'],
            y=mean_values,
            name=label,
            error_y=dict(
                type='data',
                symmetric=False,
                array=std_values,
                arrayminus=mean_values - lower_error
            )
        ))

    # Add Spanish labels
    fig.update_layout(
        title='Mejor Error de Entrenamiento y Prueba para Cada Configuración',
        xaxis_title='Numero de Capas',
        yaxis_title='Mejor Error Promedio',
        barmode='group'
    )

    # Show the plot
    fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)

    bar_plot(sys.argv[1])

