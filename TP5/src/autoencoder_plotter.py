import pandas as pd
import plotly.graph_objects as go

def plot_error(csv_file_names):
    # Read all CSV files into dataframes and concatenate them
    df_list = [pd.read_csv(file_name) for file_name in csv_file_names]
    df = pd.concat(df_list, ignore_index=True)

    # Group data by optimizer and architecture
    grouped = df.groupby(['Optimizer', 'Architecture'])

    # Create the plot
    fig = go.Figure()

    # Add a line for each group
    for name, group in grouped:
        optimizer, architecture = name
        label = f"{optimizer}, Layers: {architecture}"
        fig.add_trace(go.Scatter(x=group['Epoch'], y=group['Error'], mode='lines', name=label))

    # Update layout
    fig.update_layout(title='Error vs Epoch for Different Optimizers and Architectures',
                      xaxis_title='Epoch',
                      yaxis_title='Error',
                      plot_bgcolor='rgba(0,0,0,0)')
    fig.show()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Por favor, proporcione la ruta a los archivos CSV como argumentos.")
        sys.exit(1)

    plot_error(sys.argv[1:])

