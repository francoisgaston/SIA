import math


class SumError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    # Recibe:
    # w: np.array con los valores actuales de los w_i
    # data: todos los datos analizados para el entrenamiento
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
            if self._activation_function(w.dot(data[i])) == expected[i]:
                correct += 1
        return correct / len(data)


class QuadraticError:

    def __init__(self, activation_function=None):
        self._activation_function = activation_function

    def compute(self, data, expected, w):
        ans = 0
        for i in range(len(data)):
            ans += math.pow((expected[i] - self._activation_function(w.dot(data[i]))), 2)
        return ans/2.0


def from_str(string, activation_function):
    match string.upper():
        case "SUM": return SumError(activation_function=activation_function)
        case "ACCURACY": return AccuracyError(activation_function=activation_function)
        case "QUADRATIC": return QuadraticError(activation_function=activation_function)
        case _: return SumError(activation_function=activation_function)
