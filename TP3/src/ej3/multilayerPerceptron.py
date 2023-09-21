from ej3.layer import Layer
# MultiLayer(
#   [], [] 
#)

class MultiLayerPerceptron:
    def __init__(self, perceptrons_for_layers, activation_function):
        """ 
        perceptrons_for_layers: Un arreglo cuyo primer elemento es la cantidad de datos iniciales, y consecuentemente la cantidad de perceptrones por capa
        activation_function: The activation function to execute in the layers
        """

        # Genero los layers
        layers = []
        for index in range(1,len(perceptrons_for_layers)):
            layers.append(Layer(perceptrons_for_layers[index], perceptrons_for_layers[index-1], activation_function))
        
        self.layers = layers
        self.layers_count = len(perceptrons_for_layers)


    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x


    def backward(self, delta, x):
        # delta must be an array of (expected_i - output_i)
        for layer in self.layers[::-1]: 
            delta = layer.backward(delta)
    

    
    


    