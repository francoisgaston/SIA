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


def add_gaussian_noise(data, labels, stddev):
    if stddev == 0:
        return data, labels
    noisy_data = data + np.random.normal(0, stddev, data.shape)
    noisy_labels = labels + np.random.normal(0, stddev, labels.shape)
    return noisy_data, noisy_labels


def augment_training_data(data, labels, noise_stddev):
    noisy_data, noisy_labels = add_gaussian_noise(np.array(data), np.array(labels), noise_stddev)
    return np.concatenate((data, noisy_data)), np.concatenate((labels, noisy_labels))


def print_pixels_diff(mlp, data, do_print=False):
    if do_print:
        print("Cantidad de pixeles diferentes por dato:")
    max_diff = 0
    for i in range(len(data)):
        obtained = mlp.forward(data[i])
        if i == 1:
           if do_print:
               print(data[i], "\n", np.round(obtained), "\n\n")
        diff = 0
        for j in range(len(data[i])):
            diff += 1 if (data[i][j] != round(obtained[j])) else 0
        max_diff = max(max_diff,diff)
        # print(f"{i}: {diff} pixels")

    print(f"max_diff: {max_diff}")
    return max_diff


# Recibe la data y lo transforma en np's arrays de cada numero
def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else 0) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    return result


def split_data(data, expected, test_pct):
    # Shuffle and partition data into training and test sets
    indices = list(range(len(data)))
    random.shuffle(indices)
    split_point = int(test_pct * len(data))  # 80% for training, 20% for testing

    train_indices = indices[:split_point]
    test_indices = indices[split_point:]

    train_data = [data[i] for i in train_indices]
    train_expected = [expected[i] for i in train_indices]

    test_data = [data[i] for i in test_indices]
    test_expected = [expected[i] for i in test_indices]

    return train_data, train_expected, test_data, test_expected


def train_perceptron(config, mlp, data, expected, perceptrons_per_layer, on_epoch=None, on_min_error=None):
    if len(data) == 0:
        return []

    i = 0
    min_error = sys.float_info.max

    condition = condition_from_str(config['condition'], config['condition_config'])
    error = error_from_str(config["error"])
    limit = config["limit"]
    batch = config["batch"] if config["batch"] <= len(data) else len(data)
    optimizer = optimizer_from_str(config["optimizer"],config["optimizer_config"],config['n'],perceptrons_per_layer)

    while not condition.check_stop(min_error) and i < limit:
        final_delta_w = [np.zeros((perceptrons_per_layer[indx], perceptrons_per_layer[indx - 1] + 1)) for indx in
                         range(len(perceptrons_per_layer) - 1, 0, -1)]
        u_arr = random.sample(range(len(data)), batch)

        for u in u_arr:
            values = mlp.forward(data[u])
            aux_error = np.array(expected[u]) - np.array(values)
            gradients, _ = mlp.backward(aux_error, data[u], 1)
            deltas = optimizer.get_deltas(gradients)
            for aux in range(len(final_delta_w)):
                final_delta_w[aux] += deltas[aux]

        mlp.apply_delta_w(final_delta_w)

        new_error = error.compute(data, mlp, expected)

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
            max_diff = print_pixels_diff(mlp, data)
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            pickle_output = config["pickle_output"] + timestamp
            file_name = f"pickles/{pickle_output}"
            if(max_diff == 1):
                with open(file_name, 'wb') as file:
                    pickle.dump(mlp, file)
            print("min_error: ", min_error)

        train_perceptron(config, mlp, data, expected, perceptrons_per_layer=layers, on_epoch=None, on_min_error=on_min_error)

        def print_matrix(elem):
            for i in range(7):
                print(elem[5*i:5*(i+1)])
            print("\n-------------\n")

        for i, element in enumerate(data):
            obtained = np.round(mlp.forward(element))
            print_matrix(obtained)
            print_matrix(element)
            print(f"differing index: {np.where((obtained == 1 and abs(element) == 0) or (abs(obtained) == 0 and element == 1))}")
            print("\n--------------\n")



        weights_list = mlp.get_all_weights()

        encoder_weigths = weights_list[:len(encoder_layers)-1]
        decoder_weigths = weights_list[len(encoder_weigths):]

        encoder = MultiLayerPerceptron.from_weight_list(encoder_layers,activation_function,encoder_weigths)
        decoder = MultiLayerPerceptron.from_weight_list(decoder_layers,activation_function, decoder_weigths)

        # for weights in mlp.get_all_weights():
        #     print(weights)



