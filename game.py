import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snakepy')
clock = pygame.time.Clock()

dead = False
while not dead:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'up'
            elif event.key == pygame.K_DOWN:
                direction = 'down'
            elif event.key == pygame.K_LEFT:
                direction = 'left'
            elif event.key == pygame.RIGHT:
                direction = 'right'

    # move snake(direction)
    # draw snake
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
