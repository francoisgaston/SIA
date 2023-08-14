import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    csv["percentage"] = csv["count"]/csv["total"]
    grouped = csv.groupby(["pokemon","status_effect"])
    # nos quedamos con el minimo, maximo y media de la proporcion capturada para un pokemon y status_effect dado
    ans = grouped["percentage"].agg(["min","max","mean"]).reset_index() # agrega operando sobre la columna indicada
    ans["max_error"] = ans["max"] - ans["mean"]
    ans["min_error"] = abs(ans["min"]-ans["mean"])
    fig = go.Figure()
    for effect in ["NONE","FREEZE","SLEEP","PARALYSIS","BURN","POISON"]:
        aux = ans[ans["status_effect"]==effect]
        fig.add_trace(go.Bar(
            name=effect,
            x=aux["pokemon"],y=aux["mean"],
            error_y=dict(
                type='data',
                symmetric=False,
                array=aux["max_error"],
                arrayminus=aux["min_error"],
                visible=True
            )
        ))
    fig.update_layout(title="Status effect Vs percentage",
                      xaxis=dict(title="Pokemon"),
                      yaxis=dict(title="Captured percentage"))
    fig.show()
    #Vamos a hacer el resumen de la tendencia general para un status_effect
    #hacer un promedio con los 5 pokemons para cada status, para el punto final
    summary = csv.groupby(["status_effect"])
    summary = summary["percentage"].agg(["min","max","mean"]).reset_index()
    base = summary[summary["status_effect"]=="NONE"]["mean"].iloc[0]
    summary["factor"] = summary["mean"]/base
    print(summary)
    factors = go.Figure()
    factors.add_trace(go.Bar(
        name="hello",
        x=summary["status_effect"],y=summary["factor"])
    )
    factors.update_layout(title="Status effect Vs None",
                      xaxis=dict(title="Status effect"),
                      yaxis=dict(title="Factor of None"))
    factors.show()