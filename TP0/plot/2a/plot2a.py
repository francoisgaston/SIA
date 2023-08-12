import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    # para ver todos los datos
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        csv["average"] = csv["count"]/csv["total"]
        grouped = csv.groupby(["pokemon","status_effect"])
        print(csv.groupby(["pokemon","status_effect","pokeball"]).sum()) # solo esta para chequear
        # nos quedamos con el minimo, maximo y media de la proporcion capturada para un pokemon y status_effect dado
        ans = grouped["average"].agg(["min","max","mean"]).reset_index() # agrega operando sobre la columna indicada
        ans["max_error"] = ans["max"] - ans["mean"]
        ans["min_error"] = abs(ans["min"]-ans["mean"])
        fig = go.Figure()
        for effect in ["NONE","FREEZE","SLEEP","PARALYSIS","BURN","POISON"]:
            aux = ans[ans["status_effect"]==effect]
            print(aux["status_effect"])
            fig.add_trace(go.Bar(
                name=effect,
                x=aux["pokemon"],y=aux["mean"],
                error_y=dict(
                    type='data',  # error type: data (default), percent, constant
                    symmetric=False,  # True (default) for symmetric, False for asymmetric error bars
                    array=aux["max_error"],  # array of error values (positive direction)
                    arrayminus=aux["min_error"],  # array of error values (negative direction)
                    visible=True  # Show the error bars
                )
            ))
        fig.show()
        print(ans)
        # fig = go.Figure()

        # fig = px.scatter(ans, x="status_effect", y="mean", color="pokemon")
        # fig.show()

        #hacer un promedio con los 5 pokemons para cada status, para el punto final