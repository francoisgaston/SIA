import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys

def bar_normalize_plot(csv, variable, title, xaxis):

    # Calculate and add the ratios Visited Count / base as a new column
    plot = go.Figure()

    aux = csv.groupby(["id", variable])
    ans = aux["fitness"].agg(["min", "max", "mean"]).reset_index()
    final = csv.drop_duplicates(subset=["id"])

    for replace_type in final["id"]:
        data = ans[ans["id"] == replace_type]
        plot.add_trace(
            go.Bar(
                name=replace_type, 
                x=data[variable], 
                y=data["mean"],
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=ans["max"] - ans["mean"],
                    arrayminus=ans["mean"] - ans["min"],
                    visible=True
                )
            )
        )
    plot.update_layout(title=f"{title}"
                             f"<br><sup>Fitness obtenido para cada clase, promediado a partir de 5 ejecuciones por test</sup>",
                       xaxis=dict(title="Clase"),
                       yaxis=dict(title="Fitness promedio"),
                       legend_title="Tests")
    plot.show()

    return ans


# La idea de este codigo es generar el grafico de comparacion de fitness entre configs
# Ej: python3 src/plotter.py src/results/out_20230909231520.csv
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    ans = bar_normalize_plot(csv, "individual_class", "Fitness promedio por clase entre tests", "Class")
    print(ans)
