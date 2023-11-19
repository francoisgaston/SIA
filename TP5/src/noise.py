import numpy as np


class Noise:
    def apply(self, element):
        pass

    def apply_all(self, list):
        noisy_list = []
        for i in range(len(list)):
            noisy_list.append(self.apply(list[i]))
        return np.array(noisy_list)


class GaussianNoise(Noise):
    def __init__(self, config):
        self.stddev = config["noise_stddev"]
        self.median = config["noise_median"]

    def apply(self, element):
        return np.round(element + np.random.normal(self.median, self.stddev, element.shape))


class RandomSwitch(Noise):
    def __init__(self, config):
        self.probability = config["noise_prob"]

    def apply(self, element):
        noisy_element = []
        for item in element:
            if np.random.uniform(0, 1) <= self.probability:
                noisy_element.append(1 if item == 0 else 0)
            else:
                noisy_element.append(item)
        return np.array(noisy_element)


class SaltAndPepperNoise(Noise):
    def __init__(self, config):
        self.salt_probability = config["salt_prob"]
        self.pepper_probability = config["pepper_prob"]

    def apply(self, element):
        noisy_element = np.copy(element)
        total_pixels = noisy_element.size
        salt_pixels = int(total_pixels * self.salt_probability)
        pepper_pixels = int(total_pixels * self.pepper_probability)

        nonzero_indexes = np.flatnonzero(noisy_element)
        if nonzero_indexes.size > 0:
            salt_indices = np.random.choice(nonzero_indexes, salt_pixels, replace=False)
            noisy_element[salt_indices] = 1

        nonone_indexes = np.where(noisy_element == 0)[0]
        if nonone_indexes.size > 0:
            pepper_indices = np.random.choice(nonone_indexes, pepper_pixels, replace=False)
            noisy_element[pepper_indices] = 1

        return noisy_element


def from_str(string, config):
    match string.upper():
        case "GAUSSIAN":
            return GaussianNoise(config)
        case "RANDOM_SWITCH":
            return RandomSwitch(config)
        case "SALT_AND_PEPPER":
            return SaltAndPepperNoise(config)
        case _:
            return GaussianNoise(config)
