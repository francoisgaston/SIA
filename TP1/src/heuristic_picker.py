from heuristics.distance_heuristic import distance_heuristic
from heuristics.path_heuristic import path_heuristic
from heuristics.cos_distance_heuristic import CosineHeuristic
from heuristics.max_box_heuristic import max_box_heuristic
from heuristics.rec_path_heristic import rec_path_heuristic


class Heuristic:

    def from_string(name):
        match name:
            case "PATH":
                return path_heuristic
            case "DISTANCE":
                return distance_heuristic
            case "COSINE":
                return CosineHeuristic.apply
            case "MAX_BOX":
                return max_box_heuristic
            case "REC_PATH":
                return rec_path_heuristic
            case _:
                return distance_heuristic

