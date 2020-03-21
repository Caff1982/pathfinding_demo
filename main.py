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
        self.algo = AStar(self.grid, self.start, self.end)

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
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                # Space-bar will start the search
                if event.key == pygame.K_SPACE:
                    self.state = 'solving_maze'

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Space-bar will start the search
                    if event.key == pygame.K_SPACE:
                        self.state = 'solving_maze'

                if self.state == 'creating_maze':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = vec(pygame.mouse.get_pos()) // TILESIZE     
                        if pos in self.grid.walls:
                            self.grid.walls.remove(pos)
                        else:
                            self.grid.walls.append(pos)

            if self.state == 'solving_maze':
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