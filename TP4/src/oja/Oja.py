import numpy as np

from numpy import ndarray

class Oja:

    def __init__(self, eta_0: float, data: ndarray):
        self._eta_0 : float = eta_0
        self._data : ndarray = data
        self.weights : ndarray = self._initialize_weights(len(data[0]))
        self._epoch : int = 0
        self._eta : float = eta_0

    def _initialize_weights(self, dim: int) -> ndarray:
        return np.random.uniform(0, 1, dim)

    def _update_eta(self) -> None:
        self._epoch += 1
        self._eta = self._eta_0 / self._epoch

    def _delta_weights(self, x: ndarray, output: float) -> ndarray:
        return self._eta * output * (x - output * self.weights)

    def train(self, epoch: int = 100) -> ndarray:
        for _ in range(epoch):
            self._update_eta()
            for u in self._data:
                output = np.dot(u, self.weights)
                delta_w = self._delta_weights(u, output)
                self.weights = self.weights + delta_w

        return self.weights.copy()


