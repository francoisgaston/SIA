import numpy as np


class Perceptron:

    def __init__(self, in_count, activation_function):
        # O(Wx + b)
        self.weights = np.random.rand(1 + in_count)
        self.h = 0
        self.activation_function = activation_function

    def set_h(self, h):
        self.h = h

    def add_delta_weights(self, delta_weights):
        self.weights += delta_weights

    def get_activation(self):
        return self.activation_function.eval(self.h)

    def get_activation_diff(self):
        return self.activation_function.diff(self.h)

        # weights: [w1, ..., wn]
        # NO tiene el umbral
    def get_variable_weights(self):
        return np.copy(self.weights[1:])

    def get_h(self):
        return self.h
