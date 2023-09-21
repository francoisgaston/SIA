import numpy as np

class Perceptron:

    def __init__(self, in_count, activation_function):
        #O(Wx + b)
        self.weights = np.random.rand(in_count)
        self.h = 0
        self.delta=0
        self.activation_function = activation_function
    

    def set_h(self, h):
        self.h = h

    def set_weights(self, delta_weights):
        self.weights += delta_weights
        
    def set_delta(self, delta):
        self.delta = delta

    def get_activation(self):
        self.activation_function.eval(self.h)

    def get_activation_diff(self):
        self.activation_function.diff(self.h)

        #weights: [w0, w1, ..., wn] 
    def get_weights(self):
        return self.weights
    
    def get_h(self):
        return self.h

    def get_delta(self):
        return self.delta


    

