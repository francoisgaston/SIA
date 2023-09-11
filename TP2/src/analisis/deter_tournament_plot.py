import sys
import pandas as pd
import plotly.graph_objects as go


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    stop_condition = csv["stop_condition"].unique()[0]
    stop_condition_str = "por contenido (10 generaciones)" if stop_condition == "CHECK_CONTENT" else "por 1 segundo" if stop_condition == "MAX_TIME" else "por estructura, con una proporción de 0.9 durante 10 generaciones consecutivas"
    fitness_by_m = csv.groupby("id")["fitness"]
    ans = fitness_by_m.agg(["min", "max", "mean"]).reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ans["id"],
            y=ans["mean"],
            name="mean",
            mode="lines+markers+text",
            text=[f"{round(x, 4)}" for x in ans["mean"]],
            textposition="top center",
            textfont=dict(
                size=18,
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
        dtick=5
    )
    fig.update_layout(title=f"Fitness Vs m"
                            f"<br><sup>Promedio de fitness según m dada la condición de corte {stop_condition_str}, ejecutando 5 veces por m</sup>",
                      xaxis=dict(title="m"),
                      yaxis=dict(title="Fitness promedio")
    )
    fig.show()

