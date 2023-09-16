import sys
import pandas as pd
import plotly.graph_objects as go

RANGE = 1.1

if __name__ == "__main__":
    # Aca vamos a graficar con el csv generado a partir de adapter
    if len(sys.argv) < 2:
        print("Por favor ingrese el csv de entrada y de datos")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as data_file, open(f"{sys.argv[2]}", "r") as dots_file:
        CSV = pd.read_csv(data_file)
        dots_CSV = pd.read_csv(dots_file)
        colors = ['green' if y == 1 else 'red' for y in dots_CSV['y']]

        frames = []
        ids = CSV.drop_duplicates(subset=["Id"])
        for id in ids["Id"].tolist():
            filtered = CSV[CSV['Id'] == id]
            frames.append({
                'x': filtered['x'].tolist(),
                'y': filtered['y'].tolist()
            })

        fig = go.Figure(
            data=[go.Scatter(
                x=frames[0]['x'],
                y=frames[0]['y']
            ),
                go.Scatter(
                    x=dots_CSV['x1'],
                    y=dots_CSV['x2'],
                    mode='markers',
                    name='Puntos',
                    marker=dict(color=colors, size=10)
                )
            ],
            layout=go.Layout(
                xaxis=dict(range=[-RANGE, RANGE], autorange=False),
                yaxis=dict(range=[-RANGE, RANGE], autorange=False),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None]
                        )
                    ]
                )],
            ),
            frames=[go.Frame(data=go.Scatter(x=frame['x'], y=frame['y'])) for frame in frames[1:]]
        )
        fig.update_layout(
            xaxis=dict(
                range=[-RANGE, RANGE],
                title=dict(
                    text="X"
                )
            ),
            yaxis=dict(
                range=[-RANGE, RANGE],
                title=dict(
                    text="Y"
                )
            ),
            title="Recta de separación de clases",
        )
        fig.show()
