import numpy as np

from numpy import ndarray


def _initialize_weights(rows: int, cols: int) -> ndarray:
    cols = min(rows, max(1, cols))
    return np.random.uniform(0, 1, (rows, cols))


# https://wiki.eyewire.org/Sanger%27s_rule
class Sanger:

    def __init__(self, eta_0: float, data: ndarray, n_components: int):
        self._eta_0: float = eta_0
        self._data: ndarray = data
        self.weights: ndarray = _initialize_weights(len(data[0]), n_components if n_components is not None else len(data[0]))
        self._epoch: int = 0
        self._eta: float = eta_0

    def _update_eta(self) -> None:
        self._epoch += 1
        self._eta = self._eta_0 / self._epoch

    def _delta_weights(self, x: ndarray, output: ndarray) -> ndarray:
        rows, cols = self.weights.shape
        delta_w = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                for n in range(j+1):
                    delta_w[i, j] += self.weights[i, n] * output[n]
                delta_w[i, j] = self._eta * output[j] * (x[i] - delta_w[i, j])
        return delta_w

    def train(self, limit: int = 100) -> ndarray:
        for _ in range(limit):
            self._update_eta()
            for u in self._data:
                output = np.matmul(self.weights.T, u)
                delta_w = self._delta_weights(u, output)
                self.weights = self.weights + delta_w

        return self.weights.copy()
