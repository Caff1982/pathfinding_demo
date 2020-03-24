from collections import deque
import heapq
from settings import *
import pygame

vec = pygame.math.Vector2

class BaseAlgorithm:
    """
    Base abstract class from which the search algorithms
    can inherit
    """
    def __init__(self, graph, start, end, use_diagonals):
        self.graph = graph
        self.start = start
        self.end = end
        # Visited is a dict where keys are nodes and values
        # are the direction we came from as a vector
        # Cost is used for Dijkstra
        self.visited = {}
        self.cost = {}
        self.visited[vec2int(self.start)] = None
        self.cost[vec2int(self.start)] = 0
        self.use_diagonals = use_diagonals
        self.finished = False
        self.count = 1

    def is_finished(self):
        return self.finished

    def step(self):
        """
        Takes one step of the algorithm
        """
        raise NotImplementedError

    def get_path(self):
        """
        Draws the solution from end-tile to start-tile
        """
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = current + self.visited[vec2int(current)]

        return path


class BFS(BaseAlgorithm):
    """
    Breadth-First Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(BFS, self).__init__(graph, start, end, use_diagonals)
        self.queue = deque([self.start])

    def step(self):
        current = self.queue.popleft()
        if current == self.end:
            print('Solution found!')
            self.finished = True

        for node in self.graph.get_neighbours(current):
            if vec2int(node) not in self.visited:
                self.queue.append(node)
                self.visited[vec2int(node)] = current - node


class DFS(BaseAlgorithm):
    """
    Depth-First Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(DFS, self).__init__(graph, start, end, use_diagonals)
        self.stack = deque([self.start])

    def step(self):
        current = self.stack.pop()
        if current == self.end:
            print('Solution found!')
            self.finished = True

        for node in self.graph.get_neighbours(current):
            if vec2int(node) not in self.visited:
                self.stack.append(node)
                self.visited[vec2int(node)] = current - node


class Dijkstra(BaseAlgorithm):
    """
    Dijskstra Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(Dijkstra, self).__init__(graph, start, end, use_diagonals)
        self.frontier = PriorityQueue()
        self.frontier.put(vec2int(self.start), 0)

    def step(self):
        current = self.frontier.get()
        if current == self.end:
            print('Solution found!')
            self.finished = True

        for n in self.graph.get_neighbours(vec(current)):
                n = vec2int(n)
                n_cost = self.cost[current] + self.graph.cost(current, n)
                if n not in self.cost or n_cost < self.cost[n]:
                    self.cost[n] = n_cost
                    priority = n_cost 
                    self.frontier.put(n, priority)
                    self.visited[n] = vec(current) - vec(n)


class AStar(BaseAlgorithm):
    """
    Dijskstra Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(AStar, self).__init__(graph, start, end, use_diagonals)
        self.frontier = PriorityQueue()
        self.frontier.put(vec2int(self.start), 0)

    def heuristic(self, a, b):
        # Manhattan distance, scaled by 10 for cost
        return (abs(a.x - b.x) +  abs(a.y - b.y)) * 10

    def step(self):
        current = self.frontier.get()
        if current == self.end:
            print('Solution found!')
            self.finished = True

        for n in self.graph.get_neighbours(vec(current)):
                n = vec2int(n)
                n_cost = self.cost[current] + self.graph.cost(current, n)
                if n not in self.cost or n_cost < self.cost[n]:
                    self.cost[n] = n_cost
                    priority = n_cost + self.heuristic(self.end, vec(n))
                    self.frontier.put(n, priority)
                    self.visited[n] = vec(current) - vec(n)

class PriorityQueue:
    """
    Queue for keeping track of Dijkstra 
    search frontier using heapq
    """
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


