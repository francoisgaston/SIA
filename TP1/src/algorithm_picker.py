from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.greedy import GREEDY
from algorithms.astar import AStar


class Algorithm:

    def from_string(name):
        match name:
            case "GREEDY":
                return GREEDY
            case "A*":
                return AStar
            case "BFS":
                return BFS
            case "DFS":
                return DFS
            case _:
                return BFS

