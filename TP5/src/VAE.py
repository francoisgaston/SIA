import pickle
from datetime import datetime
import json
import numpy as np
import sys
import random
from matplotlib import pyplot as plt
from plotly import graph_objects as go

from condition import from_str as condition_from_str
from activation import from_str as activation_from_str
from error import from_str as error_from_str
from multilayerPerceptron import MultiLayerPerceptron
from optimizer import from_str as optimizer_from_str


def plot_latent_encode(encoder, data):
    elements = ['`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
               't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'DEL']
    # elements = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    fig = go.Figure()
    for i in range(len(data)):
        dots_x = []
        dots_y = []
        for j in range(50):
            output = encoder.forward(data[i])
            std = np.array(output[:2])
            mean = np.array(output[2::])
            dot = reparametrization_trick(std, mean)[1]
            dots_x.append(dot[0])
            dots_y.append(dot[1])
        fig.add_trace(go.Scatter(x=dots_x, y=dots_y, mode='markers', name=elements[i]))
    fig.show()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    fig.write_html(f"plots/latent_encoder_{timestamp}.html")


def plot_latent(decoder, n=20, output_size=15, image_size=12):
    figure = np.zeros((image_size * n, image_size * n))
    grid_x = np.linspace(-1.0, 1.0, n)
    grid_y = np.linspace(-1.0, 1.0, n)[::-1]
    # Para cada uno en la grilla
    for i, yi in enumerate(grid_y):
        for j, xi in enumerate(grid_x):
            z = np.array([[xi, yi]])
            output = decoder.forward(z)
            # Lo pasamos a matrix
            digit = output.reshape(image_size, image_size)
            # Asignamos esa parte de la figura a la imagen
            figure[i * image_size: (i + 1) * image_size, j * image_size: (j + 1) * image_size] = digit
    plt.figure(figsize=(output_size, output_size))
    start_range = image_size // 2
    end_range = n * image_size + start_range
    pixel_range = np.arange(start_range, end_range, image_size)
    # limitamos los decimales de los valores del espacio (input del decoder)
    sample_range_x = np.round(grid_x, 1)
    sample_range_y = np.round(grid_y, 1)
    # configuramos las labels para cada posicion
    plt.xticks(pixel_range, sample_range_x)
    plt.yticks(pixel_range, sample_range_y)

    plt.imshow(figure, cmap="Greys_r")
    # guardamos el archivo
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    plt.savefig(f"plots/latent_decoder_{timestamp}.png")


def loss_function(mean, std, data, result):
    rec = 0.5 * np.mean((data - result) ** 2)
    kl = -0.5 * np.sum(1 + std - mean ** 2 - np.exp(std))
    return rec + kl


def print_pixels_diff(mlp, data):
    print("Cantidad de pixeles diferentes por dato:")
    max_diff = 0
    for i in range(len(data)):
        obtained = mlp.forward(data[i])
        if i == 1:
            print(data[i], "\n", np.round(obtained), "\n\n")
        diff = 0
        for j in range(len(data[i])):
            diff += 1 if (data[i][j] != round(obtained[j])) else 0
        max_diff = max(max_diff, diff)
        # print(f"{i}: {diff} pixels")
    print(f"max_diff: {max_diff}\n")
    return max_diff


# Recibe la data y lo transforma en np's arrays de cada numero
def read_input(file, input_length):
    file1 = open(file, "r+")
    result = [(1 if character == '1' else 0) for character in file1.read().split()]
    result = np.array_split(result, len(result) / input_length)
    return result


def reparametrization_trick(std, mean):
    # eps = random.uniform(0,1)
    eps = np.random.standard_normal()
    # eps = random.uniform(-1,1)
    # eps = 0.5
    return eps, (eps * std) + mean


def train_perceptron(config, encoder, decoder, data, expected, encoder_layers, decoder_layers, on_epoch=None,
                     on_min_error=None):
    if len(data) == 0:
        return []

    i = 0
    min_error = sys.float_info.max

    condition = condition_from_str(config['condition'], config['condition_config'])
    error = error_from_str(config["error"])
    limit = config["limit"]
    batch = config["batch"] if config["batch"] <= len(data) else len(data)
    encoder_optimizer = optimizer_from_str(config["optimizer"], config["optimizer_config"], config['n'], encoder_layers)
    decoder_optimizer = optimizer_from_str(config["optimizer"], config["optimizer_config"], config['n'], decoder_layers)

    while not condition.check_stop(min_error) and i < limit:

        encoder_final_delta_w = [np.zeros((encoder_layers[indx], encoder_layers[indx - 1] + 1)) for indx in
                         range(len(encoder_layers) - 1, 0, -1)]
        decoder_final_delta_w = [np.zeros((decoder_layers[indx], decoder_layers[indx - 1] + 1)) for indx in
                                 range(len(decoder_layers) - 1, 0, -1)]

        u_arr = random.sample(range(len(data)), batch)
        loss = 0
        for u in range(len(data)):
            # Foward
            # Resultado encoder
            encoder_result = encoder.forward(data[u])
            std = np.array(encoder_result[:2])
            mean = np.array(encoder_result[2::])

            eps, z = reparametrization_trick(std, mean)

            decoder_results = decoder.forward(z)

            loss += loss_function(mean, std, data[u], decoder_results)
            # print("loss", loss)

            # Backward
            # Parte del decoder
            aux_error = np.array(expected[u]) - np.array(decoder_results)
            decoder_gradients, decoder_last_gradients_2 = decoder.backward(aux_error, z, 1, gradients=None)
            decoder_deltas = decoder_optimizer.get_deltas(decoder_gradients)
            # decoder_deltas = decoder_gradients
            decoder_last_gradients = decoder_gradients[-1]
            # TODO: fijarse si el nodo 1 es el primero de la matriz
            decoder_last_gradients = np.delete(decoder_last_gradients,0, axis=1)
            decoder_last_gradients = np.transpose(decoder_last_gradients)
            # Reparametrizacion
            # OJO: Esta hardcodeado, se asume que la segunda (despues de la capa de 2 nodos) capa del decoder tiene 4 nodos
            # dz_dm = np.ones([1,10])
            # dz_ds = eps * np.ones([1,10])
            # rt_gradients = []
            # for j in range(2):
            #     rt_gradients.append(np.dot(dz_ds,decoder_last_gradients[j])[0])
            # for j in range(2):
            #     rt_gradients.append(np.dot(dz_dm,decoder_last_gradients[j])[0])
            # dz_dm
            aux_1 = np.copy(decoder_last_gradients_2)
            # dz_ds
            aux_2 = eps * np.copy(decoder_last_gradients_2)
            aux_3 = np.concatenate((aux_2,aux_1))
            encoder_reparametrization_gradients = encoder.backward_2(None,data[u],1,gradients=np.array(aux_3))

            # Reconstruction
            dkl_dm = -1* mean
            dkl_ds = (-0.5)*(np.exp(std)-1)
            kl_gradients = np.concatenate((dkl_ds,dkl_dm))
            encoder_kl_gradients = encoder.backward_2(None,data[u],1,gradients=kl_gradients)

            # Sum gradients
            encoder_gradients = []
            for j in range(len(encoder_reparametrization_gradients)):
                encoder_gradients.append(encoder_reparametrization_gradients[j] + encoder_kl_gradients[j])
            encoder_deltas = encoder_optimizer.get_deltas(encoder_gradients)
            # encoder_deltas = encoder_gradients
            for j in range(len(encoder_final_delta_w)):
                encoder_final_delta_w[j] += encoder_deltas[j]

            # encoder_final_delta_w += encoder_deltas
            for j in range(len(decoder_final_delta_w)):
                decoder_final_delta_w[j] += decoder_deltas[j]
            # decoder_final_delta_w += decoder_deltas
        # print("loss",loss)
        encoder.apply_delta_w(encoder_final_delta_w)
        decoder.apply_delta_w(decoder_final_delta_w)

        new_error = 0
        for input_data in data:
            encoder_results = encoder.forward(input_data)
            std = np.array(encoder_results[:2])
            mean = np.array(encoder_results[2::])
            eps, z = reparametrization_trick(std, mean)
            decoder_results = decoder.forward(z)
            #for i in range(len(decoder_results)):
            #    print("exp " + str(input_data[i]) + " sal " + str(decoder_results[i]))
            #print("---------------------")
            new_error = max(new_error, error.difference(decoder_results, input_data))

        if condition.check_replace(min_error, new_error):
            if on_min_error is not None:
                on_min_error(i, new_error)
            min_error = new_error

        # encoder_optimizer.on_epoch(new_error)
        # decoder_optimizer.on_epoch(new_error)


        #     deltas = optimizer.get_deltas(gradients)
        #     for aux in range(len(final_delta_w)):
        #         final_delta_w[aux] += deltas[aux]
        #
        # mlp.apply_delta_w(final_delta_w)
        #
        # new_error = error.compute(data, mlp, expected)
        #
        # optimizer.on_epoch(new_error)

        # ### exec
        # if on_epoch is not None:
        #     # on_epoch(i, mlp, n)
        #     on_epoch(i, mlp)
        #
        # if condition.check_replace(min_error, new_error):
        #     if on_min_error is not None:
        #         on_min_error(i, mlp, new_error)
        #     min_error = new_error
        # print("i",i)
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

        encoder_layers = [config['input_length']] + config['encoder_hidden'] + [4]
        decoder_layers = [2] + config['decoder_hidden'] + [config['input_length']]

        encoder = MultiLayerPerceptron(encoder_layers, activation_function)
        decoder = MultiLayerPerceptron(decoder_layers, activation_function)

        if config["encoder_pickle_input"]:
            with open(config["encoder_pickle_input"], 'rb') as file:
                encoder = pickle.load(file)
        if  config["decoder_pickle_input"]:
            with open(config["decoder_pickle_input"], 'rb') as file:
                decoder = pickle.load(file)

        def on_min_error(epoch, min_error):
            # max_diff = print_pixels_diff(mlp, data)
            # now = datetime.now()
            # timestamp = now.strftime("%Y%m%d_%H%M%S")
            # pickle_output = config["pickle_output"] + timestamp
            # file_name = f"pickles/{pickle_output}"
            # if(max_diff == 1):
            #     with open(file_name, 'wb') as file:
            #         pickle.dump(mlp, file)
            print("min_error: ", min_error)

        if config["train"] :
            train_perceptron(config, encoder, decoder, data, expected, encoder_layers=encoder_layers, decoder_layers=decoder_layers, on_epoch=None, on_min_error=on_min_error)

        if config["encoder_pickle_output"] :
            with open("pickles/"+config["encoder_pickle_output"], 'wb') as file:
                pickle.dump(encoder, file)
        if config["decoder_pickle_output"] :
            with open("pickles/"+config["decoder_pickle_output"], 'wb') as file:
                pickle.dump(decoder, file)

        plot_latent(decoder,image_size=7)
        plot_latent_encode(encoder, data)
