import csv
import pandas as pd
import sys
import plotly.graph_objects as go

# Read the CSV file
# data = []
# with open(f"{sys.argv[1]}", "r") as csvfile:
#     reader = csv.reader(csvfile)
#     headers = next(reader)
#     for row in reader:
#         data.append(row)

# # Convert the data to a DataFrame
# df = pd.DataFrame(data, columns=headers)
# df['Execution Time'] = df['Execution Time'].astype(float)
# df['Visited Count'] = pd.to_numeric(df['Visited Count'], errors='coerce')
# df['End State Steps'] = pd.to_numeric(df['End State Steps'], errors='coerce')
# df['Forbidden points'] = df['Forbidden points'].astype(bool)


# # Modify the algorithm column to combine algorithm and heuristic if needed
# df['Algorithm_Heuristic'] = df.apply(lambda row: row['Algorithm'] if row['Algorithm'] in ['BFS', 'DFS']
#                                       else f"{row['Algorithm']} ({row['Heuristic']})", axis=1)

df = pd.read_csv(sys.argv[1])

def forbidden_points_as_string(forbidden):
    if forbidden:
        return 'Yes'
    else:
        return 'No'

# Function to plot the graph
def plot_graph(y_column, y_label):
    # Group by Mapa and Algoritmo
    # grouped_data = df.groupby(['Map', 'Forbidden points'])

    points_enabled = df.drop_duplicates(subset=["Forbidden points"])
    
    fig = go.Figure()

    base_values = df[df["Forbidden points"] == False].groupby("Map")[y_column].max()
    
    df["Ratio"] = df.apply(lambda row: row[y_column] / base_values.get(row["Map"], 1), axis=1)

    for enabled in points_enabled["Forbidden points"]:
        data = df[df["Forbidden points"] == enabled]
               
        fig.add_trace(
            go.Bar(
                name=enabled,
                x=data['Map'],
                y=data['Ratio']
            )
        )
    
    fig.update_layout(
        title=y_label,
        xaxis_title='Mapa Probado',
        yaxis_title=y_label
    )
    
    fig.show()


# Plot graph for Visited Count (Nodes Expanded)
plot_graph('Visited Count', 'Nodos Expandidos')
