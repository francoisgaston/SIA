import sys
import csv

import plotly.graph_objects as go

def plot_error(csv_file_name):
    epochs = []
    errors = []

    with open(csv_file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            epochs.append(int(row['Epoch']))
            errors.append(float(row['Error']))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs, y=errors, mode='lines', name='Error',
                             line=dict(color='LightSeaGreen')))
    fig.update_layout(title='Error vs Epoch',
                      xaxis_title='Epoch',
                      yaxis_title='Error',
                      plot_bgcolor='rgba(0,0,0,0)')
    fig.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta al archivo CSV como un argumento.")
        sys.exit(1)

    plot_error(sys.argv[1])
