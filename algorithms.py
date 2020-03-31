from collections import deque
import heapq
from settings import *
import math



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
        self.visited[self.start] = None
        self.cost[self.start] = 0
        self.use_diagonals = use_diagonals
        self.finished = False
        self.count = 1

        if self.use_diagonals:
            self.possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
                                   (1, 1), (-1, 1), (1,-1), (-1,-1)]
        else:
            self.possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def is_finished(self):
        return self.finished

    def step(self):
        """
        Takes one step of the algorithm
        """
        raise NotImplementedError

    def get_neighbours(self, node):
        neighbours = []
        for dx, dy in self.possible_moves:
            x, y = node[0] + dx, node[1] + dy
            if self.graph.is_valid(x, y) and (x, y) not in self.visited:            
                    neighbours.append((x, y))
        return neighbours

    def get_move_cost(self, a, b):
        """
        a is from node
        b is to node
        If edge is orthagonal cost is 10
        If edge is diagonal cost is 14
        """
        if ((b[0]-a[0])-(b[1]-a[1]))**2 == 1:
            return 10
        else:
            return 14

    def get_solution(self):
        """
        Draws the solution from end-tile to start-tile
        """
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            parent = self.visited[current]
            current = (current[0] + parent[0], current[1] + parent[1])
        return path


class BFS(BaseAlgorithm):
    """
    Breadth-First Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(BFS, self).__init__(graph, start, end, use_diagonals)
        self.frontier = deque([self.start])

    def step(self):
        current = self.frontier.popleft()
        if current == self.end:
            print('Solution found!')
            self.finished = True
        else:
            self.count +=1
            for node in self.get_neighbours(current):
                self.frontier.append(node)
                self.visited[node] = (current[0] - node[0], current[1] - node[1])

class DFS(BaseAlgorithm):
    """
    Depth-First Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(DFS, self).__init__(graph, start, end, use_diagonals)
        self.frontier = deque([self.start])

    def step(self):
        current = self.frontier.pop()
        if current == self.end:
            print('Solution found!')
            self.finished = True
        else:
            self.count +=1
            for node in self.get_neighbours(current):
                self.frontier.append(node)
                self.visited[node] = (current[0] - node[0], current[1] - node[1])

class Dijkstra(BaseAlgorithm):
    """
    Dijskstra Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(Dijkstra, self).__init__(graph, start, end, use_diagonals)
        self.frontier = PriorityQueue()
        self.frontier.put(self.start, 0)

    def step(self):
        current = self.frontier.get()
        if current == self.end:
            print('Solution found!')
            self.finished = True
        else:
            self.count +=1
            for n in self.get_neighbours(current):
                    move_cost = self.cost[current] + self.get_move_cost(current, n)
                    if n not in self.cost or move_cost < self.cost[n]:
                        self.cost[n] = move_cost
                        priority = move_cost 
                        self.frontier.put(n, priority)
                        self.visited[n] = (current[0] - n[0], current[1] - n[1])

class AStar(BaseAlgorithm):
    """
    Dijskstra Search algorithm
    """
    def __init__(self, graph, start, end, use_diagonals):
        super(AStar, self).__init__(graph, start, end, use_diagonals)
        self.frontier = PriorityQueue()
        self.frontier.put(self.start, 0)

    def heuristic(self, a, b):
        # Manhattan distance, scaled by 10 for cost
        dx = abs(a[0]-b[0])
        dy = abs(a[1]-b[1])
        return 10 * (dx + dy)

    def step(self):
        current = self.frontier.get()
        if current == self.end:
            print('Solution found!')
            self.finished = True
        else:
            self.count +=1
            for n in self.get_neighbours(current):
                    move_cost = self.cost[current] + self.get_move_cost(current, n)
                    if n not in self.cost or move_cost < self.cost[n]:
                        self.cost[n] = move_cost
                        priority = move_cost + self.heuristic(self.end, n)
                        self.frontier.put(n, priority)
                        self.visited[n] = (current[0] - n[0], current[1] - n[1])


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