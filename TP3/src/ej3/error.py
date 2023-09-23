import math


class SumError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    # Recibe:
    # w: np.array con los valores actuales de los w_i
    # results: todos los datos analizados para el entrenamiento
    # expected: los resultados esperados para cada dato
    def compute(self, data, expected, w):
        ans = 0
        for i in range(len(data)):
            ans += abs(expected[i] - self._activation_function.eval(w.dot(data[i])))
        return ans


class AccuracyError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    def compute(self, data, expected, w):
        correct = 0.0
        for i in range(len(data)):
            if self._activation_function.eval(w.dot(data[i])) == expected[i]:
                correct += 1
        #   Devuelve un valor entre 0 y 1, si se quiere % multiplicar por 100 y tener cuidado con la condición
        return correct / len(data)


class QuadraticError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    def compute(self, data, expected, w):
        ans = 0
        for i in range(len(data)):
            ans += math.pow((expected[i] - self._activation_function.eval(w.dot(data[i]))), 2)
        return ans/2.0


class QuadraticErrorMultilayer:
    # expected: [[]] con los valores esperados para cada caso
    def compute(self, data, mlp, expected):
        ans = 0
        for i in range(len(expected)):
            obtained = mlp.forward(data[i])
            for j in range(len(expected[i])):
                ans += (expected[i][j] - obtained[j]) ** 2
        return ans/2.0


class CrossEntropyError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    def compute(self, data, expected, w):
        ans = 0.0
        for i in range(len(data)):
            y_pred = self._activation_function.eval(w.dot(data[i]))
            y_true = expected[i]

            # Calculate the cross-entropy error for each data point and accumulate
            ans -= y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)
            
        # Average the total error for all data points
        return ans / len(data)

# Adding the CrossEntropyError to the from_str function
def from_str(string, activation_function=None):
    match string.upper():
        case "SUM": return SumError(activation_function=activation_function)
        case "ACCURACY": return AccuracyError(activation_function=activation_function)
        case "QUADRATIC": return QuadraticError(activation_function=activation_function)
        case "QUADRATIC_MULTILAYER": return QuadraticErrorMultilayer()
        case "CROSSENTROPY": return CrossEntropyError(activation_function=activation_function)
        case _: return SumError(activation_function=activation_function)
