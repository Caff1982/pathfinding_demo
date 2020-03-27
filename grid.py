from collections import deque
import pygame
from settings import *
import numpy as np


class Grid:
    def __init__(self, rows, columns):
        self.n_rows = rows
        self.n_columns = columns
        self.board = np.zeros((rows, columns))

    def is_valid(self, col, row):
        if 0 <= row < self.n_rows and 0 <= col < self.n_columns:
            if self.board[row][col] == 0:
                return True
        return False


