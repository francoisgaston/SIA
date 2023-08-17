from heuristics.distance_heuristic import distance_heuristic
from heuristics.path_heuristic import path_heuristic
from heuristics.cos_distance_heuristic import CosineHeuristic



class Heuristic:

    def from_string(name):
        match name:
            case "PATH":
                return path_heuristic
            case "DISTANCE":
                return distance_heuristic
            case "COSINE":
                return CosineHeuristic.apply

