from game import Game
from AI import AI

game = Game()
ai = AI()

winner = False
tiles_taken = 0
while winner == False:
    if tiles_taken != 9:
        coordinates = game.get_user_input()
        game.make_move('X', coordinates[0], coordinates[1])
        game.print_game_board(f"X played ({coordinates[0] + 1},{coordinates[1] + 1})")
        winner = game.check_for_winner(game.game_board)
        tiles_taken += 1

        if tiles_taken == 9:
            break
        if winner:
            break
        ai_move = ai.make_Move(game)
        game.make_move('O', ai_move[0], ai_move[1])
        game.print_game_board(f"O played ({ai_move[0] + 1},{ai_move[1] + 1})")
        winner = game.check_for_winner(game.game_board)
        tiles_taken += 1
        


if winner == False:
    game.draw()
else:
    print("Congratulations!")
    print (f"{winner} has won the match!")
    game.print_game_board("Game over")
