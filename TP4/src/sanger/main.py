import sys
import json
from Sanger import Sanger
from utils import read_input_normalize


def main():
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as file:
        config = json.load(file)

        data, _, _ = read_input_normalize(config["input"])
        n = config["eta"]
        limit = config["limit"]
        n_components = config["n_components"]

        sanger = Sanger(eta_0=n, data=data, n_components=n_components)
        eigenvectors = sanger.train(limit=limit)


if __name__ == "__main__":
    main()
