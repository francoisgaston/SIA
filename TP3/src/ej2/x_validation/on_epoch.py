import sys
import numpy as np
from numpy import ndarray

from ...utils.Function import Function


class OnEpoch:

    def exec(self, w: ndarray, epoch: int, train_data: ndarray, train_expected: ndarray, test_data: ndarray,
             test_expected: ndarray):
        pass

    def final_test_error(self):
        pass


class MseOnEpoch(OnEpoch):
    name = "Error MSE"
    label = "MSE"

    def __init__(self, activation_function: Function):
        self._final_test_error = sys.float_info.max
        self._activation_function = activation_function

    def _calculate_error(self, data: ndarray, expected: ndarray, w: ndarray):
        """
        Calculates the error of the perceptron by the MSE error function: 1/n * sum((expected - output)^2)
        """
        error = 0
        for i in range(len(data)):
            h_u = np.dot(data[i], w)
            output_u = self._activation_function.eval(h_u)
            error += (expected[i] - output_u) ** 2
        return error / len(data)

    def exec(self, w: ndarray, epoch: int, train_data: ndarray, train_expected: ndarray, test_data: ndarray,
             test_expected: ndarray):
        train_error = self._calculate_error(train_data, train_expected, w)
        test_error = self._calculate_error(test_data, test_expected, w)
        self._final_test_error = test_error
        return train_error, test_error

    def final_test_error(self):
        return self._final_test_error


class AvgMaxErrorOnEpoch(OnEpoch):
    name = "Error máximo promedio"
    label = "%"

    def __init__(self, activation_function: Function):
        self._final_test_error = sys.float_info.max
        self._activation_function = activation_function

    def _calculate_error(self, data: ndarray, expected: ndarray, w: ndarray):
        """
        Calculates the relative maximum error on average in percentage
        """
        image = self._activation_function.image
        max_error = abs(image[0] - image[1])
        error = 0
        for i in range(len(data)):
            h_u = np.dot(data[i], w)
            output_u = self._activation_function.eval(h_u)
            error += abs(expected[i] - output_u) / max_error
        return error / len(data) * 100

    def exec(self, w: ndarray, epoch: int, train_data: ndarray, train_expected: ndarray, test_data: ndarray,
             test_expected: ndarray):
        train_error = self._calculate_error(train_data, train_expected, w)
        test_error = self._calculate_error(test_data, test_expected, w)
        self._final_test_error = test_error
        return train_error, test_error

    def final_test_error(self):
        return self._final_test_error


def from_str(string: str, activation_function: Function):
    match string.upper():
        case "MSE":
            return MseOnEpoch(activation_function)
        case "AVG_MAX_ERROR":
            return AvgMaxErrorOnEpoch(activation_function)
        case _:
            raise ValueError(f"Invalid on epoch function: {string}")
