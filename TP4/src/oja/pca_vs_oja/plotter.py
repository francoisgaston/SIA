import os.path
import sys
import pandas as pd
import plotly.express as px


ROUND_TO: int = 3


def main():
    if len(sys.argv) < 1:
        print("Se requiere al menos un archivo de resultados")
        exit(1)

    results = []
    for i in range(1, len(sys.argv)):
        with open(f"{sys.argv[i]}", "r") as csv_file:
            csv = pd.read_csv(csv_file)
            eta = sys.argv[i].split("_")[-1].rsplit(".", 1)[0]
            csv["eta"] = eta
            results.append(csv)

    results = pd.concat(results)
    fig = px.line(results, x="epoch", y="error", color="eta")
    for i, d in enumerate(fig.data):
        fig.add_scatter(
            x=[d["x"][-1]],
            y=[d["y"][-1]],
            mode="markers+text",
            text=[f"<b>Distancia final<br>{round(d['y'][-1], 4)}</b>"],
            textposition="top center",
            legendgroup=d["name"],
            marker=dict(
                color=d["line"]["color"],
                size=10,
            ),
            textfont=dict(
                size=14,
                color=d["line"]["color"]
            ),
            showlegend=False,
        )
    fig.update_layout(
        title="Distancia euclídea entre el autovector de scikit-learn y el autovector de Oja",
        xaxis_title="Época",
        yaxis_title="Distancia euclídea",
        legend_title="Tasa de aprendizaje inicial",
    )
    fig.update_yaxes(
        type="log",
        exponentformat="power",
        showexponent="all",
    )
    output_dir = os.path.dirname(sys.argv[1])
    fig.write_html(f"{output_dir}/pca_vs_oja.html")


if __name__ == "__main__":
    main()
