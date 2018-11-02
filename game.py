import pygame
import time
import random
import snake_game as sg
import numpy as np

pygame.init()
display_width = 800
display_height = 600
blocksize = 10
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snakepy')
clock = pygame.time.Clock()


def map_pos(row, col):
    y = (row * blocksize) - blocksize
    x = col * blocksize
    return x, y


def draw_board(game_):
    for row in range(1, game_.board.row):
        for col in range(1, game_.board.col):
            posx, posy = map_pos(row, col)
            if game_.board.board[row][col] == 2:
                draw_block(posx, posy, blocksize, blocksize, red)
            elif game_.board.board[row][col] == 1:
                draw_block(posx, posy, blocksize, blocksize, white)


def game_over(game):
    message_display('Score: {0}'.format(game.score))

    game_loop()


def message_display(text):
    font = pygame.font.Font('freesansbold.ttf', 60)
    text_surface, text_rect = text_objects(text, font)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(2)


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def draw_block(x, y, w, h, color):
    pygame.draw.rect(game_display, color, [x, y, w, h])


def game_loop():
    board, game = sg.init(display_width/blocksize, display_height/blocksize)
    game_exit = False
    move_flag = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'up'
                    move_flag = True
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    move_flag = True
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                    move_flag = True
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    move_flag = True

        game_display.fill(black)
        if game.gameover_flag:
            game_over(game)
        if move_flag:
            game.move_snake(direction)
            # move_flag = False

        draw_board(game)
        pygame.display.update()
        clock.tick(30)


game_loop()
pygame.quit()
quit()
