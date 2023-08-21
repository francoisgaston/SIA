import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])

    # Calculate and add the ratios Visited Count / base as a new column
    plot = go.Figure()

    aux = csv.groupby(["Map", "Heuristic"])
    ans = aux["End State Steps"].agg(["min", "max", "mean"]).reset_index()
    base_values = ans[ans["Heuristic"] == "DISTANCE"].groupby("Map")["mean"].max()
    ans["Ratio"] = ans.apply(lambda row: row["mean"] / base_values.get(row["Map"], 1), axis=1)
    heuristics = csv.drop_duplicates(subset=["Heuristic"])
    print(ans)
    for heuristic in heuristics["Heuristic"]:
        data = ans[ans["Heuristic"] == heuristic]
        plot.add_trace(go.Bar(name=heuristic, x=data["Map"], y=data["Ratio"]))
    plot.update_layout(title="Heuristic Vs Steps (Normalized with optimal steps)",
                       xaxis=dict(title="Test"),
                       yaxis=dict(title="Steps / optimal_steps"))
    plot.show()
