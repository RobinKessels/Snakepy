import snake_game as sg

board = sg.Board(10, 10)
board.reset_board()

snake = sg.Snake(4)
game = sg.Game(board, snake)
game.spawn_protag()
print(game)