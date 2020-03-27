import pygame
from collections import deque
import sys
import time
from grid1 import Grid
from settings import *
from algorithms1 import BFS, DFS, AStar, Dijkstra

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
        self.grid = Grid(ROWS, COLUMNS)

        # TODO: Hardcoded for now, should choose in pygame
        self.start = (3, 18) 
        self.end = (13, 5)
        self.solution = None

        # Initialize variables to move start/end
        self.use_diagonals = True
        self.paused = False
        self.moving_start = False
        self.moving_end = False

    def draw_square(self, pos, color):
        # Scale position by tile-size
        pos = (pos[0] * TILESIZE, pos[1] * TILESIZE)
        rect = pygame.Rect(pos, (TILESIZE, TILESIZE))
        pygame.draw.rect(self.screen, color, rect)

    def update(self):
        self.screen.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.grid.board[row][col] == 1:
                    self.draw_square((col, row), BLACK)

        if self.state == 'solving_maze':
            # Draw searched tiles
            for tile in self.algo.visited:
                self.draw_square(tile, LIGHTGRAY)

        elif self.state == 'plot_solution':
            for tile in self.algo.visited:
                self.draw_square(tile, LIGHTGRAY)
            # Draw solution
            for tile in self.solution:
                self.draw_square(tile, CYAN)


        # Draw start and end squares
        self.draw_square(self.start, GREEN)
        self.draw_square(self.end, RED)
        # Draw grid-lines
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, MEDGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, MEDGRAY, (0, y), (WIDTH, y))

        pygame.display.update()


    def create_maze(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key in (pygame.K_0, pygame.K_KP0):
                    print('Using Breadth_First Search algorithm')
                    self.algo = BFS(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    print('Using Depth-First Search algorithm')
                    self.algo = DFS(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    print('Using Dijkstra algorithm')
                    self.algo = Dijkstra(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    print('Using A star algorithm')
                    self.algo = AStar(self.grid, self.start, self.end, self.use_diagonals)
                    self.state = 'solving_maze'
                elif event.key in (pygame.K_4, pygame.K_KP4):
                    print('4-way movement selected')
                    self.use_diagonals = False
                elif event.key in (pygame.K_8, pygame.K_KP8):
                    print('8-way movement selected')
                    self.use_diagonals = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // TILESIZE, pos[1] // TILESIZE)

                if self.moving_start:
                    self.start = pos
                    self.moving_start = False
                elif self.moving_end:
                    self.end = pos
                    self.moving_end = False
                elif pos == self.start:
                    self.moving_start = True
                elif pos == self.end:
                    self.moving_end = True
                
                # Add/remove walls
                elif self.grid.board[pos[1]][pos[0]] == 0:
                    self.grid.board[pos[1]][pos[0]] = 1
                elif self.grid.board[pos[1]][pos[0]] == 1:
                    self.grid.board[pos[1]][pos[0]] = 0

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // TILESIZE, pos[1] // TILESIZE)

                if self.moving_start:
                    self.start = pos
                elif self.moving_end:
                    self.end = pos

    def solve_maze(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    if self.paused:
                        print('Paused')
                        self.paused = False
                    else:
                        print('Unpaused')
                        self.paused = True
        if not self.paused:
            if not self.algo.is_finished():
                self.algo.step()
            else:
                print(f'Solution found in {self.algo.count} steps')
                print('Press Spacebar to continue')
                self.solution = self.algo.get_solution()
                self.state = 'plot_solution'
                print(self.algo.visited.keys())





    def show_solution(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.state = 'creating_maze'

    def run(self):
        while self.running:
            if self.state == 'creating_maze':
                self.create_maze()

            elif self.state == 'solving_maze':
                self.solve_maze()
                

            elif self.state == 'plot_solution':
                self.show_solution()


   

            self.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()



if __name__ == '__main__':
    app = App()
    app.run()