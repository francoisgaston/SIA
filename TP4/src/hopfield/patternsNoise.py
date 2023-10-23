import itertools
import json
import sys
import numpy as np
import pandas as pd


class PatternsNoise:
    import numpy as np

    def swap_with_gaussian(arr, probability, mean=0, std=1):
        swapped_arr = np.copy(arr)

        for i in range(arr.shape[0]):
            # for j in range(arr.shape[1]):
            if np.random.rand() < probability:
                swapped_arr[i] = np.random.normal(mean, std)

        # Replace positive values with 1 and negative values with -1
        swapped_arr[swapped_arr > 0] = 1
        swapped_arr[swapped_arr < 0] = -1
        swapped_arr[swapped_arr == 0] = arr[swapped_arr == 0]
        return swapped_arr

if __name__ == "__main__":
    # Example usage:
    N = 5
    input_array = np.array(
        [[1, -1, 1, -1, 1], [-1, 1, -1, 1, -1], [1, -1, 1, -1, 1], [-1, 1, -1, 1, -1], [1, -1, 1, -1, 1]])
    probability = 0.5  # Adjust the probability as needed
    swapped_array = PatternsNoise.swap_with_gaussian(input_array, probability)

    print("Original Array:")
    print(input_array)

    print("\nSwapped Array:")
    print(swapped_array)