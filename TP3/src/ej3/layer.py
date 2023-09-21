import numpy as np

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
    
    
    def save_h(self, hs):
        for i in range(self.perceptrons):
            self.perceptrons[i].h = hs[i]
    
        