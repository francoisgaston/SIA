import sys
import pandas as pd
import plotly.express as px

RANGE = 1.1

def add_dots(fig, dots_CSV):
    class_1_dots = dots_CSV[dots_CSV['y'] == 1]
    class_minus_1_dots = dots_CSV[dots_CSV['y'] == -1]
    fig.add_scatter(
        x=class_1_dots['x1'],
        y=class_1_dots['x2'],
        name="Clase 1",
        mode="markers",
        marker=dict(
            color="green",
            size=10,
        )
    )
    fig.add_scatter(
        x=class_minus_1_dots['x1'],
        y=class_minus_1_dots['x2'],
        name="Clase -1",
        mode="markers",
        marker=dict(
            color="red",
            size=10,
        )
    )


if __name__ == "__main__":
    # Aca vamos a graficar con el csv generado a partir de adapter
    if len(sys.argv) < 2:
        print("Por favor ingrese el csv de entrada y de datos")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as data_file, open(f"{sys.argv[2]}", "r") as dots_file:
        CSV = pd.read_csv(data_file)
        CSV["Id"] = CSV["Id"].astype(int)
        yrange = [CSV['y'].min(), CSV['y'].max()]
        fig = px.scatter(
            CSV,
            x="x",
            y="y",
            animation_frame="Id",
            range_x=[-RANGE, RANGE],
            range_y=yrange,
        )
        fig.update_layout(
            xaxis=dict(
                range=[-RANGE, RANGE],
                title=dict(
                    text="X"
                )
            ),
            yaxis=dict(
                title=dict(
                    text="Y"
                )
            ),
        )
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 300
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
        fig.layout.sliders[0].currentvalue = {
            "font": {"size": 20},
            "prefix": "Iteración: ",
            "visible": True,
            "xanchor": "right"
        }
        fig.frames[-1].layout.update(
            yaxis_range=[-RANGE, RANGE]
        )
        add_dots(fig, pd.read_csv(dots_file))
        fig.write_html("./results/animation.html")
