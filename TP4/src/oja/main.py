import sys
import json
import math
from Oja import Oja
import numpy as np
import pandas as pd


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

        oja = Oja(eta_0=n, data=data)
        autovector = oja.train(epoch=epoch)
        # print(autovector)
        base = [0.1248739,  -0.50050586,  0.40651815, -0.48287333,  0.18811162, -0.47570355,  0.27165582]
        # print(base)
        # for i in range(len(base)):
        # print(math.fabs(base[i]) - math.fabs(autovector[i]))


if __name__ == "__main__":
    main()

