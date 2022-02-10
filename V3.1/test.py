from game import Game
from AI import AI

game = Game()
ai = AI()

move = ai.make_Move(game)

board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

#move = ai.generate_game_board(board)
print(f"move[0]: {move[0]}")
print(f"move[1]: {move[1]}")