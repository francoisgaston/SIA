import os
import sys
import pandas as pd
import plotly.express as px


ROUND_TO: int = 4


def graph_pc(results: pd.DataFrame, pc_no: int, output_dir: str):
    fig = px.line(results, x="epoch", y="error", color="eta")
    for i, d in enumerate(fig.data):
        fig.add_scatter(
            x=[d["x"][-1]],
            y=[d["y"][-1]],
            mode="markers+text",
            text=[f"<b>Distancia final<br>{round(d['y'][-1], ROUND_TO)}</b>"],
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
        title=f"Distancia euclídea entre el autovector de scikit-learn y el autovector de Sanger (PC{pc_no})",
        xaxis_title="Época",
        yaxis_title="Distancia euclídea",
        legend_title="Tasa de aprendizaje inicial",
    )
    fig.update_yaxes(
        type="log",
        exponentformat="power",
        showexponent="all",
    )
    fig.write_html(f"{output_dir}/pca_vs_sanger_pc{pc_no}.html")


def main():
    if len(sys.argv) < 1:
        print("Se requiere al menos un archivo de resultados")
        exit(1)

    results_pc1 = []
    results_pc2 = []
    for i in range(1, len(sys.argv)):
        with open(f"{sys.argv[i]}", "r") as csv_file:
            csv = pd.read_csv(csv_file)
            eta, pc_no = sys.argv[i].split("_")[-1].rsplit(".", 1)[0].split("-")
            csv["eta"] = eta
            if pc_no == "pc1":
                results_pc1.append(csv)
            else:
                results_pc2.append(csv)

    results_pc1 = pd.concat(results_pc1)
    results_pc2 = pd.concat(results_pc2)
    output_dir = os.path.dirname(sys.argv[1])
    graph_pc(results_pc1, 1, output_dir)
    graph_pc(results_pc2, 2, output_dir)


if __name__ == "__main__":
    main()
