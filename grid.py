from collections import deque
import pygame
import heapq
from settings import *

vec = pygame.math.Vector2


class Node:
    def __init__(self, position):
        self.position = position
        self.x = position[1]
        self.y = position[0]
        self.Neighbours = [None, None, None, None]


class Grid:
    def __init__(self, width, height):
        self.width = width // TILESIZE
        self.height = height // TILESIZE    
        self.walls = []
        # TODO start/end to be set in pygame, hardcoded for now
        self.start = vec(3, 3) 
        self.end = vec(13, 5)
        self.possible_moves = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # Uncomment line below for diagonal movement
        # self.possible_moves += [vec(1, 1), vec(-1, 1), vec(1, -1),vec(-1, -1)]

    def get_neighbours(self, node):
        all_neighbours = [node + move for move in self.possible_moves]
        neighbours = []
        for n in all_neighbours:
            # TODO: Create helper function to filter neighbours
            if 0 <= n.x < self.width and 0 <= n.y < self.height:
                if n not in self.walls:
                    neighbours.append(n)
        return neighbours


class WeightedGrid(Grid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        """
        If edge is orthagonal cost is 10
        If edge is diagonal cost is 14
        """
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x, y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE - 3, TILESIZE - 3)
            pg.draw.rect(screen, FOREST, rect)


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

# if __name__ == '__main__':
#     g = WeightedGrid(15, 10)
#     print(g.possible_moves)