import snake_game as sg

board = sg.Board(10, 10)
board.reset_board()

game = sg.Game(board)
game.spawn_snake()
game.spawn_food()
print(game)
while 1:
    game.move_snake(input('direction = '))
    print(game)
    print(game.score)