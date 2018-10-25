import numpy as np


class Snake:
    def __init__(self, length):
        self.length = length
        self.head = np.array([0, 0])
        self.tail = np.array([0, 0])
        self.body = np.zeros((length, 2))


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = np.zeros((self.row, self.col))
        self.middle_row = self.row // 2
        self.middle_col = self.col // 2

    def __str__(self):
        return np.array2string(self.board)

    def reset_board(self):
        self.board = np.zeros((self.row, self.col))
        # Set up edge of playing field
        for i in range(0, self.row):
            self.board[i][0] = -1
            self.board[i][self.col - 1] = -1
        for i in range(0, self.col):
            self.board[0][i] = -1
            self.board[self.row - 1][i] = -1


class Game:
    def __init__(self, board, protag):
        self.board = board
        self.protag = protag
        self.score = 0

    def spawn_protag(self):
        """Spawn the protagonist default in the middle of the board"""
        for i in range(0, self.protag.length):
            self.protag.body[i] = [self.board.middle_row, self.board.middle_col + i]
            self.board.board[self.board.middle_row][self.board.middle_col + i] = 1

    def __str__(self):
        return self.board.__str__()