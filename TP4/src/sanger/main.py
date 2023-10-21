import sys
import json
import math
import numpy as np
import pandas as pd

from Sanger import Sanger


def read_input_normalize(input_file_path):
    df = pd.read_csv(input_file_path, header=None, skiprows=1)
    for column in df.columns:
        if column != 0:
            aux = df[column] - df[column].mean()
            df[column] = aux / df[column].std()
    aux = df.to_numpy()
    aux = np.delete(aux, 0, axis=1)
    names = pd.read_csv(input_file_path)
    names = names['Country']
    return aux, len(aux[0]), names


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        data, dimension, names = read_input_normalize(config["input"])
        n = config["eta"]
        epoch = config["epoch"]
        n_components = config["n_components"]

        sanger = Sanger(eta_0=n, data=data, n_components=n_components)
        eigenvectors = sanger.train(limit=epoch)

        pc1 = [0.1248739,  -0.50050586,  0.40651815, -0.48287333,  0.18811162, -0.47570355, 0.27165582]
        pc2 = [-0.1728722,  -0.13013955, -0.36965724,  0.2652478,   0.65826689,  0.08262198,  0.55320371]

        # for i in range(len(pc1)):
        # print(math.fabs(pc1[i]) - math.fabs(eigenvectors[0][i]))

        # for i in range(len(pc2)):
        # print(math.fabs(pc2[i]) - math.fabs(eigenvectors[1][i]))



if __name__ == "__main__":
    main()