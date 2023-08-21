import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    # Calculate the base values (visited count for DISTANCE) for each map
    base_values = csv[csv["Heuristic"] == "DISTANCE"].groupby("Map")["Visited Count"].max()

    # Calculate and add the ratios Visited Count / base as a new column
    csv["Ratio"] = csv.apply(lambda row: row["Visited Count"] / base_values.get(row["Map"], 1), axis=1)
    heuristics = csv.drop_duplicates(subset=["Heuristic"])
    plot = go.Figure()
    for heuristic in heuristics["Heuristic"]:
        data = csv[csv["Heuristic"] == heuristic]
        data = data[data["Algorithm"]!="BFS"] #Si quiero los datos comparado con BFS, sacar esto
        plot.add_trace(go.Bar(name=heuristic,x=data["Map"],y=data["Ratio"]))
    plot.update_layout(title="Heuristic Vs Visited ratio",
                       xaxis=dict(title="Test"),
                       yaxis=dict(title="Visited ratio (DISTANCE is base)"))
    plot.show()

    csv = csv.copy(deep=True)
    # Calculate the base values (visited count for DISTANCE) for each map
    base_values = csv[csv["Algorithm"] == "BFS"].groupby("Map")["Visited Count"].max()

    # Calculate and add the ratios Visited Count / base as a new column
    csv["Ratio"] = csv.apply(lambda row: row["Visited Count"] / base_values.get(row["Map"], 1), axis=1)
    print(csv)
    heuristics = csv.drop_duplicates(subset=["Heuristic"])
    plot = go.Figure()
    for heuristic in heuristics["Heuristic"]:
        data = csv[csv["Heuristic"] == heuristic]
        data = data[data["Algorithm"] != "BFS"]  # Si quiero los datos comparado con BFS, sacar esto
        plot.add_trace(go.Bar(name=heuristic, x=data["Map"], y=data["Ratio"]))
    data = csv[csv["Algorithm"] == "BFS"]  # Si quiero los datos comparado con BFS, sacar esto
    plot.add_trace(go.Bar(name="BFS", x=data["Map"], y=data["Ratio"]))
    plot.update_layout(title="Heuristic Vs Visited ratio",
                      xaxis=dict(title="Test"),
                      yaxis=dict(title="Visited ratio (BFS is base)"))
    plot.show()