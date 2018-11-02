import numpy as np


def init(cols, rows):
    board = Board(int(rows), int(cols))
    board.reset_board()
    game = Game(board)
    game.spawn_snake()
    game.spawn_food()
    return board, game


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
        self.gameover_flag = False
        self.tail_row = self.board.middle_row
        self.tail_col = self.board.middle_col
        self.head_row = self.board.middle_row
        self.head_col = self.board.middle_col + self.snake_length - 1
        self.body = np.zeros((self.snake_length, 2), dtype=int)
        self.score = 0
        self.prev_move = 'right'

    def __str__(self):
        return self.board.__str__()

    def spawn_snake(self):
        """Spawn the protagonist default in the middle of the board"""
        for i in range(0, self.snake_length):
            self.board.board[self.board.middle_row][self.board.middle_col + i] = 1
            self.body[i] = [self.board.middle_row, self.board.middle_col + i]

    def move_snake(self, direction):
        if self.prev_move == 'up' and direction == 'down':
            direction = 'up'
        elif self.prev_move == 'down' and direction == 'up':
            direction = 'down'
        elif self.prev_move == 'left' and direction == 'right':
            direction = 'left'
        elif self.prev_move == 'right' and direction == 'left':
            direction = 'right'
        elif not self.board.check_move(self.head_row, self.head_col, direction):
            self.game_over()
            return

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
        self.prev_move = direction

    def game_over(self):
        self.gameover_flag = True

    def spawn_food(self):
        spawned = False
        while not spawned:
            food_row = np.random.randint(1, self.board.row)
            food_col = np.random.randint(1, self.board.col)
            if self.board.board[food_row][food_col] == 0:
                self.board.board[food_row][food_col] = 2
                spawned = True

    def reset(self):
        self.board.reset_board()
        self.snake_length = 4
        self.gameover_flag = False
        self.tail_row = self.board.middle_row
        self.tail_col = self.board.middle_col
        self.head_row = self.board.middle_row
        self.head_col = self.board.middle_col + self.snake_length - 1
        self.body = np.zeros((self.snake_length, 2), dtype=int)
        self.score = 0
        self.prev_move = 'right'
        self.spawn_snake()
        self.spawn_food()
        self.score = 0

    def snake_sense(self):
        """get distances up down left right to relevant items, value of 0 means snake can't see it"""
        stop_flag = False
        food_dist = np.zeros(4, dtype=int)
        edge_dist = np.zeros(4, dtype=int)
        body_dist = np.zeros(4, dtype=int)

        # UP
        edge_dist[0] = self.head_row
        for i in range(1, self.head_row):
            value = self.board.board[self.head_row - i][self.head_col]
            if value == 2:
                food_dist[0] = i
            elif value == 1:
                if not stop_flag:
                    body_dist[0] = i
                    stop_flag = True

        # DOWN
        edge_dist[1] = (self.board.row - (self.head_row + 1)) + 1
        for i in range(self.head_row + 1, self.board.row - 1):
            value = self.board.board[i][self.head_col]
            if value == 2:
                food_dist[1] = i - self.head_row
            elif value == 1:
                if not stop_flag:
                    body_dist[1] = i - self.head_row
                    stop_flag = True

        # LEFT
        edge_dist[2] = self.head_col
        for i in range(1, self.head_col):
            value = self.board.board[self.head_row][self.head_col - i]
            if value == 2:
                food_dist[2] = i
            elif value == 1:
                if not stop_flag:
                    body_dist[2] = i
                    stop_flag = True

        # RIGHT
        edge_dist[3] = (self.board.col - (self.head_col + 1)) + 1
        for i in range(self.head_col + 1, self.board.col - 1):
            value = self.board.board[self.head_row][i]
            if value == 2:
                food_dist[3] = i - self.head_col
            elif value == 1:
                if not stop_flag:
                    body_dist[3] = i - self.head_col
                    stop_flag = True
        return body_dist, edge_dist, food_dist