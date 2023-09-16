import math
from utils import Function


class SignActivation(Function):
    def eval(self, x):
        return 1 if x >= 0 else -1

    def diff(self, x):
        return 1


class LinearActivation(Function):
    def eval(self, x):
        return x

    def diff(self, x):
        # TODO: preguntar
        return 1


class SigmoidActivation(Function):

    def __init__(self, beta):
        self._beta = beta

    def eval(self, x):
        return math.tanh(self._beta * x)

    def diff(self, x):
        return self._beta * (1 - math.pow(self.eval(x), 2))


class LogisticActivation(Function):

    def __init__(self, beta):
        self._beta = beta

    def eval(self, x):
        return 1.0 / (1 + math.exp(-2 * self._beta * x))

    def diff(self, x):
        return 2 * self._beta * self.eval(x) * (1 - self.eval(x))


def from_str(string, beta=1):
    match string.upper():
        case "SIGN":
            return SignActivation()
        case "LINEAR":
            return LinearActivation()
        case "SIGMOID":
            return SigmoidActivation(beta)
        case "LOGISTIC":
            return LogisticActivation(beta)
        case _:
            return SignActivation()
