import numpy
import numpy as np
from numpy import ndarray


class Hopfield:

    def __init__(self, patterns: ndarray, max_iterations: int):
        self.dimension = numpy.shape(patterns)[1]
        self._patterns = patterns
        self.weight_matrix = Hopfield._weight_matrix(patterns)
        self._max_iterations = max_iterations

    # If patterns is a matrix where each row is a pattern's elements, then patterns = K^T
    @staticmethod
    def _weight_matrix(patterns: ndarray) -> ndarray:
        K = numpy.transpose(patterns)
        N = numpy.shape(patterns)[1]
        pre_W = 1 / N * np.matmul(K, patterns)
        np.fill_diagonal(pre_W, 0)

        return pre_W

    @staticmethod
    def print_letter(pattern):
        for i in range(5):
            for j in range(5):
                if pattern[i * 5 + j] == 1:
                    print(" * ", end="")
                else:
                    print("   ", end="")
            print("")

    def energy_function(self, S: ndarray):
        result = 0
        for i in range(1, self.dimension):
            for j in range(i, self.dimension):
                result += self.weight_matrix[i][j] * S[i] * S[j]
        return (-1) * result

    def _pattern_found_index(self, state: ndarray) -> int:
        for idx, pattern in enumerate(self._patterns):
            if np.array_equal(state, pattern):
                return idx
        return -1

    def train(self, pattern: ndarray, on_new_state=None) -> ndarray:
        i = 0
        previous_found_idx = -1
        state = np.transpose(pattern)
        while i < self._max_iterations:
            aux = np.matmul(self.weight_matrix, state)
            aux = np.sign(aux)
            for idx, elem in enumerate(aux):
                if elem == 0:
                    aux[0][idx] = state[0][idx]
            state = aux

            if on_new_state is not None:
                on_new_state(np.transpose(state))
            pattern_found_idx = self._pattern_found_index(state)
            if pattern_found_idx != -1 and pattern_found_idx == previous_found_idx:
                break
            i += 1
            Hopfield.print_letter(state)
        return state


