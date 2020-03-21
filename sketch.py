import pygame
from collections import deque
import sys
import time
from grid import Grid
from algorithms import PriorityQueue
from settings import *

vec = pygame.math.Vector2


pygame.init()


class App:
    """
    Main class to intitialize GUI and manage state
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.solution = deque()
        self.creating_grid = True
        self.solving_grid = False

        self.grid = Grid(WIDTH, HEIGHT) 

    def draw_square(self, pos, color):
        rect = pygame.Rect(pos * TILESIZE, (TILESIZE, TILESIZE))
        pygame.draw.rect(self.screen, color, rect)

    def update(self):
        # Draw walls
        for wall in self.grid.walls:
            self.draw_square(wall, BLACK)

        
        if self.solving_grid:
            # Draw searched tiles
            for tile in self.path:
                self.draw_square(vec(tile), MEDGRAY)
            # Draw tiles still in queue as blank white
            # for tile in self.frontier:
            #     self.draw_square(vec(tile), WHITE)
            # Draw tiles in the solution
            for tile in self.solution:
                self.draw_square(vec(tile), CYAN)
        # Draw start and end squares
        # self.draw_square(self.grid.start, GREEN)
        # self.draw_square(self.grid.end, RED)

        # Draw grid-lines
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))


    def create_grid(self):
        while self.creating_grid:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    # Space-bar will start the search
                    if event.key == pygame.K_SPACE:
                        self.creating_grid = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = vec(pygame.mouse.get_pos()) // TILESIZE     
                    if pos in self.grid.walls:
                        self.grid.walls.remove(pos)
                    else:
                        self.grid.walls.append(pos)

            self.screen.fill(WHITE)
            self.update()
            pygame.display.update()

    def draw_solution(self, current):
        """
        Draws solution from end-tile to start-tile
        """
        # while current != self.grid.start:
        #     print(current)
        #     self.solution.appendleft(current)
        #     current = self.prev[current[0] * self.grid.height + current[1]]
        current = vec(current)
        print(self.path)
        while current != self.grid.start:
            print(current)
            print(type(current))
            self.solution.append(vec2int(current))
            current = current + self.path[vec2int(current)]



        self.screen.fill(WHITE)
        self.update()
        pygame.display.update()
        time.sleep(10)

    def heuristic(self, a, b):
        # Manhattan distance, scaled by 10 for cost
        return (abs(a.x - b.x) +  abs(a.y - b.y)) * 10

    def dfs_search(self):
        self.stack = deque([self.grid.start])
        self.path = {}
        self.path[vec2int(self.grid.start)] = None
        self.prev = [None] * (self.grid.height * self.grid.width)
        self.count = 1

        self.solving_grid = True
        while self.solving_grid:
            self.clock.tick(FPS)
            self.count +=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            current = self.stack.pop()
            if current == self.grid.end:       
                print('Solution Found!')
                print(f'Found solution in {self.count} steps.')
                self.draw_solution(current)
                self.solving_grid = False

            for n in self.grid.get_neighbours(current):
                if vec2int(n) not in self.path:
                    self.stack.append(n)
                    self.path[vec2int(n)] = current - n
                    self.prev[(vec2int(n)[0] * self.grid.height + vec2int(n)[1])] = vec2int(current)

            self.screen.fill(WHITE)
            self.update()
            pygame.display.update()
        
    def bfs_search(self):
        self.frontier = deque([self.grid.start])
        # self.frontier.append(self.grid.start)
        self.path = {}
        self.path[vec2int(self.grid.start)] = None
        self.prev = [None] * (self.grid.height * self.grid.width)
        self.count = 1

        self.solving_grid = True
        while self.solving_grid:
            self.clock.tick(FPS)
            self.count +=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            current = self.frontier.popleft()
            if current == self.grid.end:       
                print('Solution Found!')
                print(f'Found solution in {self.count} steps.')
                self.draw_solution(current)
                self.solving_grid = False

            for n in self.grid.get_neighbours(current):
                if vec2int(n) not in self.path:
                    self.frontier.append(n)
                    self.path[vec2int(n)] = current - n
                    self.prev[(vec2int(n)[0] * self.grid.height + vec2int(n)[1])] = vec2int(current)

            self.screen.fill(WHITE)
            self.update()
            pygame.display.update()

    def dijkstra_search(self):
        self.frontier = PriorityQueue()
        self.frontier.put(vec2int(self.grid.start), 0)
        self.prev = [None] * (self.grid.height * self.grid.width)
        self.path = {}
        self.cost = {}
        self.path[vec2int(self.grid.start)] = None
        self.cost[vec2int(self.grid.start)] = 0
        self.count = 1

        self.solving_grid = True
        while self.solving_grid:
            self.clock.tick(FPS)
            self.count +=1

            current = self.frontier.get()
            if current == self.grid.end:
                print(f'Solution found in {self.count} steps.')
                self.draw_solution(current)
                self.soving_grid = False


            for n in self.grid.get_neighbours(vec(current)):
                n = vec2int(n)
                n_cost = self.cost[current] + self.grid.cost(current, n)
                if n not in self.cost or n_cost < self.cost[n]:
                    self.cost[n] = n_cost
                    priority = n_cost 
                    self.frontier.put(n, priority)
                    self.path[n] = vec(current) - vec(n)
                    self.prev[(n[0] * self.grid.height + n[1])] = current

            self.screen.fill(WHITE)
            self.update()
            pygame.display.update()

    def a_star_search(self):
        self.frontier = PriorityQueue()
        self.frontier.put(vec2int(self.grid.start), 0)
        self.prev = [None] * (self.grid.height * self.grid.width)
        self.path = {}
        self.cost = {}
        self.path[vec2int(self.grid.start)] = None
        self.cost[vec2int(self.grid.start)] = 0
        self.count = 1

        self.solving_grid = True
        while self.solving_grid:
            self.clock.tick(FPS)
            self.count +=1

            current = self.frontier.get()
            if current == self.grid.end:
                print(f'Solution found in {self.count} steps.')
                self.draw_solution(current)
                self.soving_grid = False


            for n in self.grid.get_neighbours(vec(current)):
                n = vec2int(n)
                n_cost = self.cost[current] + self.grid.cost(current, n)
                if n not in self.cost or n_cost < self.cost[n]:
                    self.cost[n] = n_cost
                    priority = n_cost + self.heuristic(self.grid.end, vec(n))
                    self.frontier.put(n, priority)
                    self.path[n] = vec(current) - vec(n)
                    self.prev[(n[0] * self.grid.height + n[1])] = current

            self.screen.fill(WHITE)
            self.update()
            pygame.display.update()

if __name__ == '__main__':
    app = App()
    app.create_grid()
    # app.dfs_search()
    # app.bfs_search()
    app.dijkstra_search()
    # app.a_star_search()
    time.sleep(10)
    sys.exit()