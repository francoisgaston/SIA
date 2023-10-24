import sys
import json
from .Oja import Oja
from .utils import read_input_normalize


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        data, dimension, names = read_input_normalize(config["input"])
        n = config["eta"]
        limit = config["limit"]

        oja = Oja(eta_0=n, data=data)
        eigenvector = oja.train(limit=limit)

        print(f"El autovector de PC1 es: {eigenvector.round(3).tolist()}")


if __name__ == "__main__":
    main()
