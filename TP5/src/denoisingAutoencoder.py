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
from utils.PrintLetter import plot_pattern


def train_perceptron(config, mlp, data, expected, perceptrons_per_layer, on_epoch=None, on_min_error=None):
    if len(data) == 0:
        return []

    i = 0
    min_error = sys.float_info.max
    new_error = sys.float_info.max

    condition = condition_from_str(config['condition'], config['condition_config'])
    error = error_from_str(config["error"])
    limit = config["limit"]
    batch = config["batch"] if config["batch"] <= len(data) else len(data)
    optimizer = optimizer_from_str(config["optimizer"], config["optimizer_config"], config['n'], perceptrons_per_layer)
    noise = noise_from_str(config["noise"], config["noise_config"])

    while not condition.check_stop(new_error) and i < limit:
        final_delta_w = [np.zeros((perceptrons_per_layer[indx], perceptrons_per_layer[indx - 1] + 1)) for indx in
                         range(len(perceptrons_per_layer) - 1, 0, -1)]
        u_arr = random.sample(range(len(data)), batch)

        for u in u_arr:
            noisy_value = noise.apply(data[u])
            values = mlp.forward(noisy_value)
            aux_error = np.array(expected[u]) - np.array(values)
            gradients, _ = mlp.backward(aux_error, data[u], 1)
            deltas = optimizer.get_deltas(gradients)
            for aux in range(len(final_delta_w)):
                final_delta_w[aux] += deltas[aux]

        mlp.apply_delta_w(final_delta_w)

        noisy_data = noise.apply_all(data)
        new_error = error.compute(noisy_data, mlp, expected)
        print(f"Epoch {i} - Error: {new_error}")

        optimizer.on_epoch(new_error)

        ### exec
        if on_epoch is not None:
            # on_epoch(i, mlp, n)
            on_epoch(i, mlp)

        if condition.check_replace(min_error, new_error):
            if on_min_error is not None:
                on_min_error(i, mlp, new_error)
            min_error = new_error

        i += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor ingrese el archivo de configuración")
        exit(1)

    with open(sys.argv[1], "r") as config:
        config = json.load(config)
        data = np.array(read_input(config['input'], config['input_length']))
        expected = np.copy(data)
        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])

        # make layers symmetric
        encoder_layers = config['perceptrons_for_layers']
        decoder_layers = config['perceptrons_for_layers'][::-1]
        layers = encoder_layers + decoder_layers[1::]
        mlp = MultiLayerPerceptron(layers, activation_function)


        # if(config["pickle_input"]):
        #     with open(config["pickle_input"], 'rb') as file:
        #         mlp = pickle.load(file)

        def on_min_error(epoch, mlp, min_error):
            # max_diff = print_pixels_diff(mlp, data)
            print("min_error: ", min_error)


        train_perceptron(config, mlp, data, expected, perceptrons_per_layer=layers, on_epoch=None,
                         on_min_error=on_min_error)


        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        pickle_output = f"{config['pickle_output']}_{timestamp}.pkl"
        with open(pickle_output, 'wb') as file:
            pickle.dump(mlp, file)

        # weights_list = mlp.get_all_weights()

        # encoder_weigths = weights_list[:len(encoder_layers) - 1]
        # decoder_weigths = weights_list[len(encoder_weigths):]

        # encoder = MultiLayerPerceptron.from_weight_list(encoder_layers, activation_function, encoder_weigths)
        # decoder = MultiLayerPerceptron.from_weight_list(decoder_layers, activation_function, decoder_weigths)
