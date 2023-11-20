import pickle
from datetime import datetime
import json
import numpy as np
import sys
import random

from condition import from_str as condition_from_str
from activation import from_str as activation_from_str
from error import from_str as error_from_str
from multilayerPerceptron import MultiLayerPerceptron
from optimizer import from_str as optimizer_from_str
from autoencoder import read_input, print_pixels_diff
from noise import from_str as noise_from_str

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(sys.argv[1], "r") as config:
        config = json.load(config)
        _input = config['input']
        _input_length = config['input_length']
        noise = noise_from_str(config["noise"], config["noise_config"])
    # with open('pickles/mlp_max_diff_1.pkl20231120_151625', 'rb') as file:
    with open('pickles/mlp_max_diff_1.pkl20231120_154628', 'rb') as file:

        mlp = pickle.load(file)
        data = np.array(read_input(_input, _input_length))
        print("##########################Test with NO NOISE###########################")
        for i in range(len(data)):
            def round_to_one_or_zero(x):
                return 1 if x >= 0.5 else 0
            result = mlp.forward(data[i])
            result = np.vectorize(round_to_one_or_zero)(result)

            if np.array_equal(data[i], result):
                print("Same")
            else:
                print("Different")
                print("\t\t\t", "X: --------------------------------------------------------------------")
                print("\t\t\t", data[i])
                print("\t\t\t", "Obtained: -------------------------------------------------------------")
                print("\t\t\t", result)
        print("############################Test with NOISE#############################")
        noisy_data = noise.apply_all(data)
        for i in range(len(data)):
            def round_to_one_or_zero(x):
                return 1 if x >= 0.5 else 0
            result = mlp.forward(noisy_data[i])
            result = np.vectorize(round_to_one_or_zero)(result)

            if np.array_equal(data[i], result):
                print("Denoised")
            else:
                print("Not Denoised")
                print("\t\t\t X: --------------------------------------------------------------------")
                print("\t\t\t", data[i])
                print("\t\t\t Noisy: --------------------------------------------------------------------")
                print("\t\t\t", noisy_data[i])
                print("\t\t\t Obtained: -------------------------------------------------------------")
                print("\t\t\t", result)
