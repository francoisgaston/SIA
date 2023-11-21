import numpy as np
from perceptron import Perceptron

class Layer:

    def __init__(self, numbers_perceptrons, numbers_weights, activation_function):
        
        perceptrons = []
        for index in range(numbers_perceptrons):
            perceptrons.append(Perceptron(numbers_weights, activation_function))
        
        self.perceptrons = perceptrons
        self.activation_function = np.vectorize(activation_function.eval)
        # self.activation_function = activation_function.eval


    def create_weights_matrix(self):
        weights_matriz = []
        for perceptron in self.perceptrons:
            # aca perceptron_weigths va a tener a [w0, w1, ..., wn] es decir tiene al umbral
            # Tampoco devuelve una deep compy, todos los cambios se van a reflejar 
            weights_matriz.append(perceptron.weights)
        
        return np.array(weights_matriz)
    
    
    def forward(self, x):
        # x must be a np array
        x = np.insert(x, 0, 1)
        # results = []
        # for perceptron in self.perceptrons:
        #     results.append(perceptron.weights.dot(x))
        matrix = self.create_weights_matrix()
        results = np.matmul(matrix, x) #h_i, entrada de la otra capa
        self.save_h(results)
        results = self.activation_function(results)
        # for i in range(len(results)):
        #     results[i] = self.activation_function(results[i])
        return results

    
    # d: vector con los delta de la capa superior
    # prev_weights: pesos de la capa superior [i][j] es el peso de la neurona i de la capa siguiente (de arriba) a la neurona j de la capa actual (se mira al reves aca)
    # n: Tasa de aprendizaje
    # next_activations: Son los theta(h) de los nodos de la capa inferior, incluyendo el 1 para w_0
    def backward(self, d, prev_weights, n, next_activations):
        pre_d = np.matmul(prev_weights, d) #TODO: revisar, en el mural esta al reves
        # pre_d = []
        # for j in range(len(d)):
        #     aux = 0
        #     for i in range(len(prev_weights)):
        #         aux += prev_weights[i][j] * d[j]
        #     pre_d.append(aux)

        # ESTE ES EL QUE VA
        # for j in range(len(prev_weights[0])):
        #     aux = 0
        #     for i in range(len(d)):
        #         aux += d[i] * prev_weights[i][j] #todos los que llegan a la actual son estos
        #     pre_d.append(aux)
        # for i in range(len(prev_weights)):
        #     aux = 0
        #     for j in range(len(prev_weights[i])):
        #         aux += prev_weights[i][j] * d[i]
        #     pre_d.append(aux)



        perceptrons_activation_diff = self.get_perceptrons_activation_diff()
        # Las siguientes dos lineas hacen lo siguiente:
        #   for index in range(len(perceptrons_activation_diff)):
        #       d.append(pre_d[index] * perceptrons_activation_diff[index])

        perceptrons_activation_diff_diagonal = np.diag(perceptrons_activation_diff)
        d = np.matmul(pre_d, perceptrons_activation_diff_diagonal)
        #d = []
        #for i in range(len(pre_d)):
        #    d.append(pre_d[i] * perceptrons_activation_diff[i])

        #d_n = []
        #for d_i in d:
        #    d_n.append(d_i * n)
        d_n = n * d

        # delta_w = np.matmul(pre_delta_weights, next_activations)
        delta_w = np.matmul(np.split(d_n, len(d_n)), np.split(next_activations, 1))
        #delta_w = []
        #for i in range(len(d_n)):
        #    delta_w.append([])
        #    for j in range(len(next_activations)):
        #        delta_w[i].append(d_n[i] * next_activations[j])

        return np.array(delta_w), np.array(d)
    
    
    def save_h(self, hs):
        for i in range(len(self.perceptrons)):
            self.perceptrons[i].h = hs[i]

    
    def get_perceptrons_activation(self):
        activation = [perceptron.get_activation() for perceptron in self.perceptrons]
        activation = np.array(activation)
        # Agrego el 1 en la posicion 0
        # Entonces tengo a las variaciones de los pesos en la posicion 0
        return np.insert(activation, 0, 1)
    

    def get_perceptrons_activation_diff(self):
        activation_diff = [perceptron.get_activation_diff() for perceptron in self.perceptrons]
        return np.array(activation_diff)


    def get_perceptrons_weights(self):
        weights = [perceptron.get_variable_weights() for perceptron in self.perceptrons]
        return np.array(weights)

    def get_perceptrons_weights_with_bias(self):
        weights = [perceptron.get_variable_weights_with_bias() for perceptron in self.perceptrons]
        return np.array(weights)

    def set_perceptron_weights(self, weights):
        # set all weigths (with bias)
        for i, perceptron in enumerate(self.perceptrons):
            perceptron.set_weights(weights[i])

    def get_perceptron_weights_transposed(self):
        aux = self.get_perceptrons_weights()
        return np.transpose(aux)

    
    def add_perceptrons_delta_weights(self, delta_weights):
        for i, perceptron in enumerate(self.perceptrons):
            perceptron.add_delta_weights(delta_weights[i])
        