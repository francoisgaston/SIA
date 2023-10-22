import sys
import json
import os
import csv
from datetime import datetime
import numpy as np

from numpy import ndarray
from ..Oja import Oja
from ..utils import read_input_normalize

scikit_pc1: ndarray = np.array([0.1248739, -0.50050586, 0.40651815, -0.48287333, 0.18811162, -0.47570355, 0.27165582])


def euclidean_distance(x: ndarray, y: ndarray) -> float:
    return np.linalg.norm(x - y)


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        data, dimension, names = read_input_normalize(config["input"])
        etas = config["etas"]
        limit = config["limit"]
        output_dir = config["output"]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        headers = ["epoch", "error"]
        for i in range(len(scikit_pc1)):
            headers.append(f"a_{i+1}")

        for eta in etas:
            print(f"Training with eta={eta}")
            CSV = f"{output_dir}/pca_vs_oja_{timestamp}_{eta}.csv"
            os.makedirs(os.path.dirname(CSV), exist_ok=True)
            with open(CSV, "w", newline='') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(headers)

                oja = Oja(eta_0=eta, data=data)

                def on_epoch(epoch, weights):
                    error = euclidean_distance(weights, scikit_pc1)
                    print(f"Epoch {epoch}: {error}")
                    csv_writer.writerow([epoch, error] + weights.tolist())

                oja.train(limit=limit, on_epoch=on_epoch)


if __name__ == "__main__":
    main()
