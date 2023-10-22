import itertools
import json
import sys
import numpy as np
import pandas as pd

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
        try_file = config["try"]
        combination_size = config["combination_size"]

        patterns = read_input(input_file, input_length)
        letters = {chr(97 + i): patterns[i] for i in range(26)}
        pattern_to_try = read_input(try_file, input_length)
        max_iterations = config["max_iterations"]

        combinations = list(itertools.combinations(letters.keys(), combination_size))
        avg_list = []
        for combination in combinations:
            # print(combination, end="")
            patterns_combination = [np.array(letters[key]) for key in combination]
            max_product, min_product, avg_product = Hopfield._analyse_orthogonality(np.array(patterns_combination))
            # print(" => Max: ", end="")
            # print(max_product, end="")
            # print(" | Min: ", end="")
            # print(min_product, end="")
            # print(" | Avg: ", end="")
            # print(avg_product)
            avg_list.append((avg_product, combination))
        df = pd.DataFrame(sorted(avg_list), columns=["|<,>| avg", "combination"])
        # df.head(15).style.format({'|<,>| avg': "{:.2f}"}).hide(axis='index')
        print(df.head(55))
        print(df.tail(15))


        # hopfield = Hopfield(patterns, max_iterations)
        #
        # energy_results = []
        #
        # # Hopfield train hook
        # def on_new_state(state):
        #     # Calculate energy function after every new state
        #     energy_results.append(hopfield.energy_function(state))
        #
        #
        # hopfield.train(pattern_to_try[0], on_new_state)
        #
        # for pattern in patterns:
        #     Hopfield.print_letter(pattern)
        #
        # print(energy_results)