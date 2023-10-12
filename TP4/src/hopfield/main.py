import json
import sys
import numpy as np

from hopfield import Hopfield

def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else -1) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    print(result)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Falta el archivo de configuración")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        input_file = config["input"]
        input_length = config["size"]

        patterns = read_input(input_file, input_length)
        max_iterations = config["max_iterations"]
        hopfield = Hopfield(patterns, max_iterations)

        energy_results = []

        # Hopfield train hook
        def on_new_state(state):
            # Calculate energy function after every new state
            energy_results.append(hopfield.energy_function(state))


        hopfield.train(patterns[0], on_new_state)

        for pattern in patterns:
            Hopfield.print_letter(pattern)

        print(energy_results)
