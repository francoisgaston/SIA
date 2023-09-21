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

def from_str(string, activation_function=None):
    match string.upper():
        case "SUM": return SumError(activation_function=activation_function)
        case "ACCURACY": return AccuracyError(activation_function=activation_function)
        case "QUADRATIC": return QuadraticError(activation_function=activation_function)
        case "QUADRATIC_MULTILAYER": return QuadraticErrorMultilayer()
        case _: return SumError(activation_function=activation_function)
