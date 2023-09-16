# Creates a class with functions to check the condition to stop
# the algorithm and to replace the current value of the algorithm

class NonAccuracyCondition:
    def __init__(self, epsilon):
        self._epsilon = epsilon

    def check_stop(self, curr_error):
        return curr_error < self._epsilon

    def check_replace(self, curr_error, new_error):
        return new_error < curr_error


# To be used in accuracy error, where we want a higher value
class AccuracyCondition:
    def __init__(self, epsilon):
        self._epsilon = epsilon

    def check_stop(self, curr_error):
        return curr_error >= self._epsilon

    def check_replace(self, curr_error, new_error):
        return new_error > curr_error

def from_str(string, epsilon):
    match string.upper():
        case "ACCURACY": return AccuracyCondition(epsilon=epsilon)
        case _: return NonAccuracyCondition(epsilon=epsilon)