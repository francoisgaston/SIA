import json
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from hopfield import Hopfield
from patternsNoise import PatternsNoise

def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else -1) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    return result

def plot_pattern(pattern, iteration, save_path="plots"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    pattern_reshaped = pattern.reshape((5, 5))
    plt.imshow(pattern_reshaped, cmap='gray_r')
    plt.axis('off')
    filename = os.path.join(save_path, f"pattern_{iteration}.png")
    plt.savefig(filename)
    plt.close()

def aggregate_plots(iteration_count, save_path="plots", grid_filename="grid_plot.png"):
    rows = (iteration_count // 4) + int(iteration_count % 4 != 0)
    fig, axes = plt.subplots(rows, 4, figsize=(20, 5*rows))
    
    for i in range(rows * 4):
        row = i // 4
        col = i % 4
        ax = axes[row, col] if rows > 1 else axes[col]
        
        if i < iteration_count:
            img = plt.imread(os.path.join(save_path, f"pattern_{i}.png"))
            ax.imshow(img)
            ax.set_title(f"Iteration {i}")
        
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, grid_filename))
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing configuration file")
        exit(1)

    with open(f"{sys.argv[1]}", "r") as config_file:
        config = json.load(config_file)
        input_file = config["input"]
        input_length = config["size"]
        try_file = config["try"]
        noise = config["noise"]
        
        patterns = read_input(input_file, input_length)
        pattern_to_try = read_input(try_file, input_length)

        if noise is True:
            pattern_to_try = PatternsNoise.swap_with_gaussian(pattern_to_try[0], config["probability_of_noise"])
        else:
            pattern_to_try = pattern_to_try[0]

        max_iterations = config["max_iterations"]
        hopfield = Hopfield(patterns, max_iterations)

        energy_results = []

        # Hopfield train hook
        def on_new_state(state, iteration):
            # Calculate energy function after every new state
            energy_results.append(hopfield.energy_function(state))
            plot_pattern(np.array(state), iteration)

        print("Input pattern: ")
        plot_pattern(pattern_to_try, 0)

        hopfield.train(pattern_to_try, on_new_state)

        # Aggregate all saved plots into a grid
        aggregate_plots(len(energy_results))

        print(energy_results)
