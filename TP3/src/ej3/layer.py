import numpy as np
from perceptron import Perceptron

class Layer:

    def __init__(self, numbers_perceptrons, numbers_weights, activation_function):
        
        perceptrons = []
        for index in range(numbers_perceptrons):
            perceptrons.append(Perceptron(numbers_weights, activation_function))
        
        self.perceptrons = perceptrons
        self.activation_function = np.vectorize(activation_function.eval)


    def create_weights_matriz(self):
        weights_matriz = []
        for perceptron in self.perceptrons:
            # aca perceptron_weigths va a tener a [w0, w1, ..., wn] es decir tiene al umbral
            # Tampoco devuelve una deep compy, todos los cambios se van a reflejar 
            weights_matriz.append(perceptron.weights)
        
        return np.array(weights_matriz)
    
    
    def forward(self, x):
        # x must be an np array
        x = np.insert(x, 0, 1)
        matrix = self.create_weights_matriz()
        results = np.matmul(matrix, x) #h_i, entrada de la otra capa
        self.save_h(results)
        results = self.activation_function(results)
        return results

    
    # d: vector con los delta de la capa superior
    # prev_weights: pesos de la capa superior 
    # n: Tasa de aprendizaje
    # next_activations: Son los theta(h) de los nodos de la capa inferior, incluyendo el 1 para w_0
    def backward(self, d, prev_weights, n, next_activations):
        pre_d = np.matmul(prev_weights, d)
        perceptrons_activation_diff = self.get_perceptrons_activation_diff()
        # Las siguientes dos lineas hacen lo siguiente:
        #   for index in range(len(perceptrons_activation_diff)):
        #       d.append(pre_d[index] * perceptrons_activation_diff[index])
        perceptrons_activation_diff_diagonal = np.diag(perceptrons_activation_diff)
        d = np.matmul(pre_d, perceptrons_activation_diff_diagonal)
        pre_delta_weights = n * d
        delta_w = np.matmul(pre_delta_weights, next_activations)
        return delta_w, d
    
    
    def save_h(self, hs):
        for i in range(len(self.perceptrons)):
            self.perceptrons[i].h = hs[i]

    
    def get_perceptrons_activation(self):
        activation = [perceptron.get_activation() for perceptron in self.perceptrons]
        activation = np.array(activation)
        return np.insert(activation, 0, 1)
    

    def get_perceptrons_activation_diff(self):
        activation_diff = [perceptron.get_activation_diff() for perceptron in self.perceptrons]
        return np.array(activation_diff)


    def get_perceptrons_weights(self):
        weights = [perceptron.get_variable_weights() for perceptron in self.perceptrons]
        return np.array(weights)

    
    def add_perceptrons_delta_weights(self, delta_weights):
        for i, perceptron in enumerate(self.perceptrons):
            perceptron.add_delta_weights(delta_weights[i])
        