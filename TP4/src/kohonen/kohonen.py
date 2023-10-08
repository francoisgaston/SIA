import math
import random
import sys
import numpy as np

from numpy import ndarray
from Perceptron import Perceptron


# Given two points, calculates the euclidean distante between two points
# d = sqrt((p2_x - p1_x)^2 + (p2_y - p1_y)^2)
def distance(p1: (int, int), p2: (int, int)) -> float:
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


class Kohonen:

    # size: size of matrix (size x size)
    # radius: radius to update neurons
    # eta: learning rate
    # data: if none => random weights
    def __init__(self, size: int = 1, radius: float = None, eta: float = None, dimension: int = 1,
                 mult_iterations: int = 1, data: ndarray = None):
        self._update_eta = eta is None
        self._update_radius = radius is None
        self._radius = radius if radius is not None else size
        self._eta = eta if eta is not None else 1
        self.epoch = 1
        self.size = size
        self._dimension = dimension
        self.perceptrons = np.empty((size, size), dtype=object)
        if data is None:
            self._init_random_weights()
        else:
            self._init_data_weights_(data)
        self.mult_iterations = mult_iterations

    def _init_random_weights(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.perceptrons[i][j] = Perceptron(np.random.uniform(0, 1, self._dimension))
                # self.perceptrons[i][j] = Perceptron(np.ones(self._dimension))

    def _init_data_weights_(self, data: ndarray) -> None:
        perceptrons_count = len(self.perceptrons)
        data_count = len(data)
        if data_count < perceptrons_count:
            raise Exception("KxK must be lower or equal to P")

        aux_data = data.copy()
        for i in range(perceptrons_count):
            for j in range(len(self.perceptrons[i])):
                rand_index = np.random.randint(0, high=data_count)
                element = aux_data[rand_index]
                self.perceptrons[i][j] = Perceptron(np.copy(element))
                aux_data = np.delete(aux_data, rand_index, 0)
                print(self.perceptrons[i][j].weights)

    # Given the radius and the winner perceptron coordinates (tuple),
    # update the weights of the perceptron neighbourhood according to n (eta) and the input (x)
    def _update_neighbourhood(self, center: (int, int), x: ndarray) -> None:
        floor_radius = math.floor(self._radius)
        for a in range(max(0, center[0] - floor_radius), min(self.size, center[0] + floor_radius + 1)):
            for b in range(max(0, center[1] - floor_radius), min(self.size, center[1] + floor_radius + 1)):
                if distance(center, (a, b)) <= self._radius:
                    self.perceptrons[a][b].update_weights(self._eta, x)

    def _update_variables(self) -> None:
        self.epoch += 1
        self._update_radius_function()
        self._update_eta_function()

    def _update_eta_function(self) -> None:
        if self._update_eta:
            self._eta = min(self._eta / self.epoch, 1)

    def _update_radius_function(self) -> None:
        if self._update_radius:
            self._radius = max(self.size / self.epoch, 1)

    def train(self, data) -> None:
        if len(data) == 0: return
        assert len(data[0]) == self._dimension

        # TODO: ver si lo hacemos de tandas
        # for _ in range(self.mult_iterations):
        #     for register in data:
        #         i, j = self.find_winner_percepton(register)

        for _ in range(self.mult_iterations * len(data)):
            register = data[random.randint(0, len(data) - 1)]
            row, col = self._find_winner_perceptron(register)
            self._update_neighbourhood((row, col), register)
            self._update_variables()

    def get_activations(self, data) -> ndarray:
        if len(data) == 0: return np.empty((self.size, self.size), dtype=int)
        assert len(data[0]) == self._dimension

        results = np.zeros((self.size, self.size), dtype=int)
        for register in data:
            row, col = self._find_winner_perceptron(register)
            results[row][col] += 1
        return results

    def get_u_matrix(self):
        ans = np.zeros((self.size, self.size))

        for i in range(self.size):
            for j in range(self.size):
                # Para cada perceptron, calculamos la distancia promedio a sus vecinas
                sum = 0.0
                count = 0
                for delta_row in range(-1, 2):
                    for delta_col in range(-1, 2):
                        row, col = i + delta_row, j + delta_col
                        if 0 <= row <= self.size - 1 and 0 <= col <= self.size - 1:
                            sum += self.perceptrons[i][j].similarity(self.perceptrons[row][col].weights)
                            count += 1
                ans[i][j] = sum / count

        return ans

    def _find_winner_perceptron(self, x: ndarray) -> (int, int):
        winner = (-1, -1)
        min_distance = sys.float_info.max
        for i in range(self.size):
            for j in range(self.size):
                distance = self.perceptrons[i][j].similarity(x)
                if distance < min_distance:
                    min_distance = distance
                    winner = (i, j)
        return winner
