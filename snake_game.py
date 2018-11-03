import numpy as np
import game as g
import pygame


def init(cols, rows):
    board = Board(int(rows), int(cols))
    board.reset_board()
    game = Game(board)
    game.spawn_snake()
    game.spawn_food()
    return game


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
        self.reward = 0

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
        if not self.board.check_move(self.head_row, self.head_col, direction):
            self.game_over()
            self.reward -= 1
            return

        new_row, new_col = get_next_pos(self.head_row, self.head_col, direction)
        # Delete tail on board if there is no food
        if self.board.board[new_row][new_col] != 2:
            self.board.board[self.tail_row][self.tail_col] = 0
            self.body = self.body[1:]
            self.tail_row = self.body[0][0]
            self.tail_col = self.body[0][1]
            self.reward -= 0
        elif self.board.board[new_row][new_col] == 2:
            self.board.board[new_row][new_col] = 1
            self.spawn_food()
            self.score += 1
            self.reward += 5
        # Make new head on board
        self.board.board[new_row][new_col] = 1
        self.head_row = new_row
        self.head_col = new_col
        self.body = np.vstack([self.body, [self.head_row, self.head_col]])
        self.prev_move = direction

    def game_over(self):
        self.gameover_flag = True
        #self.reward = -1

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
        self.reward = 0
        return self.snake_sense()

    def step(self, direction):
        self.move_snake(direction)
        return self.snake_sense(), self.reward, self.gameover_flag

    def snake_sense(self):
        """get distances up down left right to relevant items, value of 0 means snake can't see it"""
        distances = np.zeros(24, dtype = int)

        # UP
        stop_flag = False
        stop_food_flag = False
        distances[8] = self.head_row
        for i in range(1, self.head_row):
            value = self.board.board[self.head_row - i][self.head_col]
            if value == 2:
                if not stop_food_flag:
                    distances[16] = i
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[0] = i
                    stop_flag = True

        # UP RIGHT
        stop_flag = False
        stop_food_flag = False
        if self.board.col - self.head_col > self.head_row:
            distances[9] = self.head_row
        else:
            distances[9] = self.head_col
        row = self.head_row
        col = self.head_col
        while row > 0 and col < self.board.col - 1:
            row -= 1
            col += 1
            value = self.board.board[row][col]
            if value == 2:
                if not stop_food_flag:
                    distances[17] = col - self.head_col
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[1] = col - self.head_col
                    stop_flag = True

        # RIGHT
        stop_flag = False
        stop_food_flag = False
        distances[10] = (self.board.col - (self.head_col + 1)) + 1
        for i in range(self.head_col + 1, self.board.col - 1):
            value = self.board.board[self.head_row][i]
            if value == 2:
                if not stop_food_flag:
                    distances[18] = i - self.head_col
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[2] = i - self.head_col
                    stop_flag = True

        # RIGHT DOWN
        stop_flag = False
        stop_food_flag = False
        if self.board.col - self.head_col > self.board.row - self.head_row:
            distances[11] = self.board.row - self.head_row
        else:
            distances[11] = self.board.col - self.head_col
        row = self.head_row
        col = self.head_col
        while row < self.board.row - 1 and col < self.board.col - 1:
            row += 1
            col += 1
            value = self.board.board[row][col]
            if value == 2:
                if not stop_food_flag:
                    distances[17] = row - self.head_row
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[3] = row - self.head_row
                    stop_flag = True

        # DOWN
        stop_flag = False
        stop_food_flag = False
        distances[12] = (self.board.row - (self.head_row + 1)) + 1
        for i in range(self.head_row + 1, self.board.row - 1):
            value = self.board.board[i][self.head_col]
            if value == 2:
                if not stop_food_flag:
                    distances[20] = i - self.head_row
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[4] = i - self.head_row
                    stop_flag = True

        # DOWN LEFT
        stop_flag = False
        stop_food_flag = False
        if self.head_col > self.board.row - self.head_row:
            distances[13] = self.board.row - self.head_row
        else:
            distances[13] = self.board.col - self.head_col
        row = self.head_row
        col = self.head_col
        while row < self.board.row - 1 and col > 0:
            row += 1
            col -= 1
            value = self.board.board[row][col]
            if value == 2:
                if not stop_food_flag:
                    distances[21] = row - self.head_row
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[5] = row - self.head_row
                    stop_flag = True

        # LEFT
        stop_flag = False
        stop_food_flag = False
        distances[6] = self.head_col
        for i in range(1, self.head_col):
            value = self.board.board[self.head_row][self.head_col - i]
            if value == 2:
                if not stop_food_flag:
                    distances[22] = i
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[14] = i
                    stop_flag = True

        # LEFT UP
        stop_flag = False
        stop_food_flag = False
        if self.head_col > self.head_row:
            distances[13] = self.head_row
        else:
            distances[15] = self.board.col - self.head_col
        row = self.head_row
        col = self.head_col
        while row > 0 and col > 0:
            row -= 1
            col -= 1
            value = self.board.board[row][col]
            if value == 2:
                if not stop_food_flag:
                    distances[23] = self.head_row - row
                    stop_food_flag = True
            elif value == 1:
                if not stop_flag:
                    distances[7] = self.head_row - row
                    stop_flag = True

        #for i in range(24):
            #if distances[i] == 0:
              #  distances[i] = -1
        return distances

    def render(self):
        black = (0, 0, 0)
        clock = pygame.time.Clock()
        game_display = pygame.display.set_mode((230, 230))
        game_display.fill(black)
        g.draw_board(self)
        pygame.display.update()
        clock.tick(60)

