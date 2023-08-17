from abc import ABC, abstractmethod


class Heuristics(ABC):
    @staticmethod
    @abstractmethod
    def apply(initial_state):
        pass
