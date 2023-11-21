import os.path
import sys
import pickle
import json
import numpy as np
import plotly.graph_objects as go

from activation import from_str as activation_from_str
from multilayerPerceptron import MultiLayerPerceptron
from autoencoder import read_input
from noise import from_str as noise_from_str
from utils.PrintLetter import plot_pattern


def plot(encoder, decoder, data, noise, latent_file, pattern_file):
    fonts = ['`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
             'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
             't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'DEL']
    fig = go.Figure()
    for i in range(len(data)):
        dots_x = []
        dots_y = []
        min_y_idx = 0
        for j in range(5):
            noisy_value = noise.apply(data[i])
            enc_output = encoder.forward(noisy_value)
            dots_x.append(enc_output[0])
            dots_y.append(enc_output[1])
            min_y_idx = j if dots_y[j] < dots_y[min_y_idx] else min_y_idx
            dec_output = decoder.forward(enc_output)
            plot_pattern(dec_output, (7,5), f"{pattern_file}{fonts[i] if fonts[i] != '|' else 'pipe'}_{j}.png")
        fig.add_trace(go.Scatter(x=dots_x, y=dots_y, mode='markers', name=fonts[i]))
        fig.add_annotation(x=dots_x[min_y_idx], y=dots_y[min_y_idx], text=fonts[i], showarrow=False, font=dict(size=20))
    fig.update_layout(title='Espacio latente', xaxis_title='x', yaxis_title='y')
    path = os.path.dirname(latent_file)
    if not os.path.exists(path):
        os.makedirs(path)
    fig.write_html(f"{latent_file}.html")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Por favor ingrese el archivo de configuración y el pickle")
        exit(1)

    with open(sys.argv[1], "r") as file:
        config = json.load(file)

        encoder_layers = config['perceptrons_for_layers']
        decoder_layers = config['perceptrons_for_layers'][::-1]

        activation_function = activation_from_str(string=config['activation'], beta=config["beta"])
        data = np.array(read_input(config['input'], config['input_length']))
        noise = noise_from_str(config["noise"], config["noise_config"])

        mlp = pickle.load(open(sys.argv[2], "rb"))

        weights = mlp.get_all_weights()
        encoder_weights = weights[:len(encoder_layers) - 1]
        decoder_weights = weights[len(encoder_weights):]

        encoder = MultiLayerPerceptron.from_weight_list(encoder_layers, activation_function, encoder_weights)
        decoder = MultiLayerPerceptron.from_weight_list(decoder_layers, activation_function, decoder_weights)

        plot(encoder, decoder, data, noise, f"plots/denoising_latent_space/{config['noise']}_20", f"plots/denoising_pattern/{config['noise']}_20/")
