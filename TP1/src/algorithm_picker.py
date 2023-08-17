from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.greedy import GREEDY
from algorithms.astar import AStar


class Algorithm:

    def from_string(name, initial_state):
        match name:
            case "GREEDY":
                return GREEDY.solve(initial_state)
            case "A*":
                return AStar.solve(initial_state)
            case "BFS":
                return BFS.solve(initial_state)
            case "DFS":
                return DFS.solve(initial_state)

