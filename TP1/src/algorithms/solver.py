from abc import ABC, abstractmethod


class Solver(ABC):
    @staticmethod
    @abstractmethod
    def solve(initial_state):
        pass
