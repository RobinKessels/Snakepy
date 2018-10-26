import numpy as np


def get_next_pos(row, col, direction):
    if direction == 'up':
        return row - 1, col
    elif direction == 'down':
        return row + 1, col
    elif direction == 'left':
        return row, col - 1
    elif direction == 'right':
        return row, col + 1


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = np.zeros((self.row, self.col), dtype=int)
        self.middle_row = self.row // 2
        self.middle_col = self.col // 2

    def __str__(self):
        return np.array2string(self.board)

    def reset_board(self):
        self.board = np.zeros((self.row, self.col), dtype=int)

    def check_move(self, row, col, direction):
        new_pos_row, new_pos_col = get_next_pos(row, col, direction)
        if new_pos_row < 0 or new_pos_row > self.row - 1 or new_pos_col < 0 or new_pos_col > self.col - 1:
            return False
        if self.board[new_pos_row][new_pos_col] == 1:
            return False
        else:
            return True


class Game:
    def __init__(self, board):
        self.board = board
        self.snake_length = 4
        self.tail_row = self.board.middle_row
        self.tail_col = self.board.middle_col
        self.head_row = self.board.middle_row
        self.head_col = self.board.middle_col + self.snake_length - 1
        self.body = np.zeros((self.snake_length, 2), dtype=int)
        self.score = 0
        self.prev_move = ''

    def __str__(self):
        return self.board.__str__()

    def spawn_snake(self):
        """Spawn the protagonist default in the middle of the board"""
        for i in range(0, self.snake_length):
            self.board.board[self.board.middle_row][self.board.middle_col + i] = 1
            self.body[i] = [self.board.middle_row, self.board.middle_col + i]

    def move_snake(self, direction):
        if self.prev_move == 'up' and direction == 'down':
            return
        elif self.prev_move == 'down' and direction == 'up':
            return
        elif self.prev_move == 'left' and direction == 'right':
            return
        elif self.prev_move == 'right' and direction == 'left':
            return
        if not self.board.check_move(self.head_row, self.head_col, direction):
            self.game_over()
        else:
            new_row, new_col = get_next_pos(self.head_row, self.head_col, direction)
            # Delete tail on board if there is no food
            if self.board.board[new_row][new_col] != 2:
                self.board.board[self.tail_row][self.tail_col] = 0
                self.body = self.body[1:]
                self.tail_row = self.body[0][0]
                self.tail_col = self.body[0][1]

            elif self.board.board[new_row][new_col] == 2:
                self.board.board[new_row][new_col] = 1
                self.spawn_food()
                self.score += 1
            # Make new head on board
            self.board.board[new_row][new_col] = 1
            self.head_row = new_row
            self.head_col = new_col
            self.body = np.vstack([self.body, [self.head_row, self.head_col]])
        self.prev_move == direction

    def game_over(self):
        print("rip")

    def spawn_food(self):
        spawned = False
        while not spawned:
            food_row = np.random.randint(1, self.board.row)
            food_col = np.random.randint(1, self.board.col)
            if self.board.board[food_row][food_col] == 0:
                self.board.board[food_row][food_col] = 2
                spawned = True