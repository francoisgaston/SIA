import pandas as pd
import sys
import plotly.express as px

def plot_error_from_csv_with_plotly(csv_filepath):
    df = pd.read_csv(csv_filepath)
    
    if all(column in df.columns for column in ['epoca', 'error_training']):
        
        fig = px.line(df, x='epoca', y=['error_training'], 
                      labels={'value': 'Error', 'epoca': 'Epoch'},
                      title='Error over Epochs')
        
        # Show the plot
        fig.show()
        
    else:
        print("Required columns ('epoca', 'error_training', 'error_test') not found in CSV.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo ")
        exit(1)

    
    # Replace this with the path to your CSV file
    csv_filepath = f"{sys.argv[1]}"
    
    plot_error_from_csv_with_plotly(csv_filepath)

