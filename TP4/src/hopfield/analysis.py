import itertools
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from hopfield import Hopfield

def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else -1) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
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
            patterns_combination = [np.array(letters[key]) for key in combination]
            max_product, min_product, avg_product = Hopfield._analyse_orthogonality(np.array(patterns_combination))
            avg_list.append((avg_product, combination))
        df = pd.DataFrame(sorted(avg_list), columns=["|<,>| avg", "combination"])
        
        # Visualize top 55 combinations
        plt.figure(figsize=(15,6))
        df.head(55).plot(x='combination', y='|<,>| avg', kind='bar', figsize=(15, 6))
        plt.title("Top 55 Combinations based on Average Orthogonality")
        plt.ylabel("|<,>| avg")
        plt.xlabel("Combinations")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

        # Visualize bottom 15 combinations
        plt.figure(figsize=(10,4))
        df.tail(15).plot(x='combination', y='|<,>| avg', kind='bar', figsize=(10, 4))
        plt.title("Bottom 15 Combinations based on Average Orthogonality")
        plt.ylabel("|<,>| avg")
        plt.xlabel("Combinations")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
