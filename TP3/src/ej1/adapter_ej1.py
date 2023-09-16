import sys
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import sys
import os

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
            for x in np.linspace(-1.2, 1.2, 100):
                ans.append([row['Id'], x, (row['w1'] * x + row['w0'])/(-row['w2'])])


        headers = ["Id", "x", "y"]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        CSV = './results/' + "plotter_" + timestamp + ".csv"
        os.makedirs(os.path.dirname(CSV), exist_ok=True)
        with open(CSV, "w", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(headers)
            csv_writer.writerows(ans)
