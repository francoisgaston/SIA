import numpy as np

from numpy import ndarray


def _initialize_weights(dim: int) -> ndarray:
    return np.random.uniform(0, 1, dim)


class Oja:

    def __init__(self, eta_0: float, data: ndarray):
        self._eta_0: float = eta_0
        self._data: ndarray = data
        self.weights: ndarray = _initialize_weights(len(data[0]))
        self._epoch: int = 0
        self._eta: float = eta_0

    def _update_eta(self) -> None:
        self._epoch += 1
        self._eta = self._eta_0 / self._epoch

    def _delta_weights(self, x: ndarray, output: float) -> ndarray:
        return (self._eta * output * (x - output * self.weights)).astype(float)

    def train(self, limit: int = 100, on_epoch: callable = None) -> ndarray:
        for i in range(limit):
            if on_epoch is not None:
                on_epoch(i, self.weights.copy())
            self._update_eta()
            for u in self._data:
                output = np.dot(u, self.weights)
                delta_w = self._delta_weights(u, output)
                self.weights = self.weights + delta_w

        return self.weights.copy()
