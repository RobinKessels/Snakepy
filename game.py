import pygame
import time

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snakepy')
clock = pygame.time.Clock()


def game_over():
    message_display('Snake has died..')
    game_loop()


def message_display(text):
    font = pygame.font.Font('freesansbold.ttf', 80)
    text_surface, text_rect = text_objects(text, font)
    text_rect.center = ((display_width/2), (display_height/2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(2)


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def game_loop():
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'

        # move snake(direction)
        # draw snake

        # if x > display_width or x < 0:
         #   game_over()
        game_display.fill(black)
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
