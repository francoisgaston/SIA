import math
import numpy as np

from numpy import ndarray


# Given two vectors, calculates the norm between both of them: || x1 - x2 ||
def norm(x1: ndarray, x2: ndarray) -> float:
    return np.linalg.norm(x1 - x2)


class Perceptron:
    SIMILARITY = "EUCLIDES"

    def __init__(self, weights: ndarray):
        self.weights = weights
        self._similarity_fun = Perceptron.exp_similarity if Perceptron.SIMILARITY.upper() == "EXP" else Perceptron.euclides_similarity

    @staticmethod
    def euclides_similarity(w: ndarray, x: ndarray) -> float:
        return norm(w, x)

    @staticmethod
    def exp_similarity(w: ndarray, x: ndarray) -> float:
        return math.exp(-math.pow(Perceptron.euclides_similarity(w, x), 2))

    def update_weights(self, n: float, x: ndarray) -> None:
        self.weights = self.weights + n * (x - self.weights)

    def similarity(self, x: ndarray) -> float:
        return self._similarity_fun(self.weights, x)
