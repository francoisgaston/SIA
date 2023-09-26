import pandas as pd
import numpy as np
import sys
from utils.write_csv import write_csv

# Run the script: python -m src.ej1.adapter_ej1 [csv_file]

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Por favor ingrese el csv de entrada")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as data_file:
        # 1 w0 w1 w2 -> puntos
        # 2 w0 w1 w2 -> puntos
        # 3 w0 w1 w2 -> puntos
        csv_data = pd.read_csv(data_file)
        start_x = -1.2
        end_x = 1.2
        # 0 = w2 * y + w1 * x + w0 -> y = (w1 * x + w0)/(-w2)
        ans = []
        for index, row in csv_data.iterrows():
            for x in np.linspace(-1.2, 1.2, 1000):
                ans.append([row['Id'], x, (row['w1'] * x + row['w0']) / (-row['w2'])])

        headers = ["Id", "x", "y"]
        filename = "src/ej1/results/plotter_" + "_".join(sys.argv[1].split("/")[-1].split(".")[0].split("_")[:-1])
        write_csv(filename, headers, ans)
