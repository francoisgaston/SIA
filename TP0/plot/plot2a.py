import plotly as plt
import pandas as pd
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the csv input.")
        sys.exit(1)

    csv = pd.read_csv(sys.argv[1])
    # para ver todos los datos
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        csv["average"]= csv["count"]/csv["total"]
        grouped = csv.groupby(["pokemon","status_effect"])
        print(csv.groupby(["pokemon","status_effect","pokeball"]).sum()) # solo esta para chequear
        # nos quedamos con el minimo, maximo y media de la proporcion capturada para un pokemon y status_effect dado
        ans = grouped["average"].agg(["min","max","mean"]) # agrega operando sobre la columna indicada
        print(ans)
