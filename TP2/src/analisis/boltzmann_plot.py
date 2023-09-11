import sys
import pandas as pd
import plotly.graph_objects as go

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    constant = sys.argv[1].split("_")[1]
    fitness_by_constant = csv.groupby("id")["fitness"]
    ans = fitness_by_constant.agg(["min", "max", "mean"]).reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ans["id"],
            y=ans["mean"],
            name="mean",
            mode="lines+markers+text",
            text=[f"{round(x, 2)}" for x in ans["mean"]],
            textposition="top center",
            textfont=dict(
                size=14,
                color="black"
            ),
            error_y=dict(
                type='data',
                symmetric=False,
                array=ans["max"] - ans["mean"],
                arrayminus=ans["mean"] - ans["min"],
                visible=True
            )
        )
    )
    fig.update_xaxes(
        dtick=0.1
    )
    fig.update_layout(title=f"Fitness Vs {constant} "
                            f"<br><sup>Hallando el valor de las constantes para la ecuación de Boltzmann</sup>"
                            f"<br><sup>Resultados obtenidos con 10 ejecuciones, mostrando el promedio de fitness</sup>",
                        xaxis=dict(title=constant),
                        yaxis=dict(title="Fitness promedio"))
    fig.show()


