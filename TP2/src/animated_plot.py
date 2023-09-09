import sys
import json
import io
import os
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime

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
        duration=200,
        loop=0,
        optimize=True,
    )
    fig.layout.sliders[0].update(active=0)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Por favor ingrese el archivo de configuración y el csv de entrada")
        exit(1)

    with (open(f"{sys.argv[1]}", "r") as config_file, open(f"{sys.argv[2]}", "r") as csv_file):
        config = json.load(config_file)
        csv = pd.read_csv(csv_file)
        csv["id_config"] = 'Test #' + csv["id_config"].astype(str)
        ans = csv.groupby(["id_config", "generations", "id"]).first().reset_index()
        range_y = [-5.0, 150.0]
        if config["attribute"] == "fitness":
            range_y = [-5.0, 60.0]
        elif config["attribute"] == "height":
            range_y = [1.2, 2.2]
        fig = px.scatter(
            ans,
            x="id",
            y=config["attribute"],
            animation_frame="generations",
            color="id_config",
            symbol="id_config",
            range_y=range_y,
            labels={"id_config": "Tests"},
        )
        fig.update_layout(
            title=f"Convergencia de {config['attribute']} a lo largo de las generaciones"
                  f"<br><sup>Los individuos se muestran ordenados por fitness, de mayor a menor.</sup>",
            xaxis=dict(title="n-ésimo individuo con mayor fitness"),
            yaxis=dict(title=config["attribute"]),
        )
        if config["attribute"] == "height":
            fig.update_yaxes(
                dtick = 0.05
            )
        else:
            fig.update_yaxes(
                dtick = 5
            )
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 300
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
        generate_gif(fig, config["output"])



