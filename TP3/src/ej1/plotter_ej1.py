import sys
import io
import os
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime

RANGE = 1.1

def generate_gif(fig, output):
    frames = []
    for s, fr in enumerate(fig.frames):
        fig.update(data=fr.data)
        fig.layout.sliders[0].update(active=s)
        frames.append(Image.open(io.BytesIO(fig.to_image(format="png"))))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    GIF = output + "_" + timestamp + ".gif"
    os.makedirs(os.path.dirname(GIF), exist_ok=True)
    frames[0].save(
        GIF,
        save_all=True,
        append_images=frames[1:],
        duration=300,
        loop=0,
        optimize=True,
    )
    fig.layout.sliders[0].update(active=0)

if __name__ == "__main__":
    # Aca vamos a graficar con el csv generado a partir de adapter
    if len(sys.argv) < 2:
        print("Por favor ingrese el csv de entrada y de datos")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as data_file, open(f"{sys.argv[2]}", "r") as dots_file:
        CSV = pd.read_csv(data_file)
        dots_CSV = pd.read_csv(dots_file)
        colors = ['green' if y == 1 else 'red' for y in dots_CSV['y']]
        fig = px.scatter(
            CSV,
            x="x",
            y="y",
            animation_frame="Id",
            range_x=[-RANGE, RANGE],
            range_y=[-RANGE, RANGE],
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
        )
        generate_gif(fig, "./results/animation")
