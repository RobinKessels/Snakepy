import numpy as np


class Snake:
    def __init__(self, length):
        self.length = length
        self.head = np.array([0, 0])
        self.tail = np.array([0, 0])


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = np.zeros((row, col))

    def __str__(self):
        return print(self.board)

