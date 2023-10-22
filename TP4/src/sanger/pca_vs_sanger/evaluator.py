import json
import os
import sys
import csv
import numpy as np
from ..utils import read_input_normalize
from datetime import datetime
from ..Sanger import Sanger

from numpy import ndarray

scikit_pc1: ndarray = np.array([0.1248739, -0.50050586, 0.40651815, -0.48287333, 0.18811162, -0.47570355, 0.27165582])
scikit_pc2: ndarray = np.array([-0.1728722, -0.13013955, -0.36965724, 0.2652478, 0.65826689, 0.08262198, 0.55320371])


def euclidean_distance(x: ndarray, y: ndarray) -> float:
    return np.linalg.norm(np.absolute(x) - np.absolute(y))


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        data, dimension, names = read_input_normalize(config["input"])
        etas = config["etas"]
        limit = config["limit"]
        n_components = config["n_components"]
        output_dir = config["output"]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        headers = ["epoch", "error"]
        for i in range(len(scikit_pc1)):
            headers.append(f"a_{i+1}")

        for eta in etas:
            print(f"Training with eta={eta}")
            PC1_CSV = f"{output_dir}/pca_vs_oja_{timestamp}_{eta}-pc1.csv"
            PC2_CSV = f"{output_dir}/pca_vs_oja_{timestamp}_{eta}-pc2.csv"
            os.makedirs(os.path.dirname(PC1_CSV), exist_ok=True)
            os.makedirs(os.path.dirname(PC2_CSV), exist_ok=True)
            with open(PC1_CSV, "w", newline='') as pc1_of, open(PC2_CSV, "w", newline='') as pc2_of:
                pc1_csv_writer = csv.writer(pc1_of)
                pc2_csv_writer = csv.writer(pc2_of)
                pc1_csv_writer.writerow(headers)
                pc2_csv_writer.writerow(headers)

                sanger = Sanger(eta_0=eta, data=data, n_components=n_components)

                def on_epoch(epoch, weights):
                    pc1 = weights[:, 0].T
                    pc2 = weights[:, 1].T
                    error_pc1 = euclidean_distance(pc1, scikit_pc1)
                    error_pc2 = euclidean_distance(pc2, scikit_pc2)
                    print(f"Epoch {epoch}: {error_pc1}\t{error_pc2}")
                    pc1_csv_writer.writerow([epoch, error_pc1] + pc1.tolist())
                    pc2_csv_writer.writerow([epoch, error_pc2] + pc2.tolist())

                sanger.train(limit=limit, on_epoch=on_epoch)


if __name__ == "__main__":
    main()
