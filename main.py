import pygame
from collections import deque
import sys
import time
from grid import Grid
from settings import *
from algorithms import BFS, DFS, Dijkstra, AStar

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
        self.caption = pygame.display.set_caption('Maze Solver')
        self.state = 'creating_maze'
        self.running = True
        self.grid = Grid(WIDTH, HEIGHT)

        # TODO: Hardcoded for now, should choose in pygame
        self.start = vec(3, 3) 
        self.end = vec(13, 5)

        # Initialize class variables to move start/end
        self.use_diagonals = False
        self.moving_start = False
        self.moving_end = False

    def draw_square(self, pos, color):
        rect = pygame.Rect(pos * TILESIZE, (TILESIZE, TILESIZE))
        pygame.draw.rect(self.screen, color, rect)

    def update(self):
        self.screen.fill(WHITE)
        # Draw walls
        for wall in self.grid.walls:
            self.draw_square(wall, BLACK)

        if self.state == 'solving_maze':
            # Draw searched tiles
            for tile in self.algo.visited:
                self.draw_square(vec(tile), MEDGRAY)
            # Draw tiles still in queue as blank white
            # for tile in self.frontier:
            #     self.draw_square(vec(tile), WHITE)

            # Draw tiles in the solution
            if self.algo.is_finished():
                self.state = 'finished'
                path = self.algo.get_path()
                for tile in path:
                    self.draw_square(tile, CYAN)

        # Draw start and end squares
        self.draw_square(self.start, GREEN)
        self.draw_square(self.end, RED)
        # Draw grid-lines
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

        pygame.display.update()

    def create_maze(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_a:
                    print('Using A star algorithm')
                    self.algo = AStar(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key == pygame.K_b:
                    print('Using Breadth_First Search algorithm')
                    self.algo = BFS(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key == pygame.K_d:
                    print('Using Dijkstra Search algorithm')
                    self.algo = Dijkstra(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key == pygame.K_4:
                    print('4-way movement selected')
                    self.use_diagonals = False
                elif event.key == pygame.K_8:
                    print('8-way movement selected')
                    self.use_diagonals = True


            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = vec(pygame.mouse.get_pos()) // TILESIZE
                if self.moving_start:
                    self.start = pos
                    self.moving_start = False
                elif self.moving_end:
                    self.end = pos
                    self.moving_end = False

                elif pos in self.grid.walls:
                    self.grid.walls.remove(pos)
                elif pos == self.start:
                    self.moving_start = True
                elif pos == self.end:
                    self.moving_end = True
                else:
                    self.grid.walls.append(pos)

            elif event.type == pygame.MOUSEMOTION:
                pos = vec(pygame.mouse.get_pos()) // TILESIZE
                if self.moving_start:
                    self.start = pos
                elif self.moving_end:
                    self.end = pos

    def run(self):
        while self.running:
            if self.state == 'creating_maze':
                self.create_maze()

            elif self.state == 'solving_maze':
                self.algo.step()
            elif self.state == 'finished':
                time.sleep(10)
                self.state = 'creating_maze'
   

            self.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()