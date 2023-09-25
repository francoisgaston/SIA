import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys

def plot_errors_from_csv(csv_filepath):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_filepath)
    
    # Get unique configuration IDs
    unique_config_ids = df['config_id'].unique()
    
    for config_id in unique_config_ids:
        # Filter the DataFrame based on config_id
        df_filtered = df[df['config_id'] == config_id]
        
        # Sort by epoch
        df_filtered = df_filtered.sort_values('epoca')
        
        # Plot using Plotly
        fig = px.line(df_filtered, x='epoca', y=['error_training', 'error_test'],
                      labels={'value': 'Error', 'epoca': 'Epoch'},
                      title=f"Training and Test Error for Config {config_id}")

        # Update the layout to make the x-axis logarithmic
        fig.update_layout(xaxis_type="log",
                          xaxis_title="Log Epoch")
        
        fig.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the CSV file as an argument.")
        sys.exit(1)
    
    csv_filepath = sys.argv[1]
    plot_errors_from_csv(csv_filepath)

