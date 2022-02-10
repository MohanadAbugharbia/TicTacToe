import time

from numpy import tile
from game import Game
from AI import AI
from escapesequences import escapesequences

start_time = time.time()

game = Game()
ai = AI()
es = escapesequences()
def play_again():
    while True:
        answer = input("Do you want to play again? (y/n): ")
        if answer == 'y' or answer =='Y':
            return True
        elif answer == 'n' or answer == 'N':
            return False
        else:
            print("Please answer with Y or N.")


es.CLEAR()
es.HOME()

game.print_game_board("Welcome by Tic-Tac-Toe\nYou are player X\n")
run = True
while run:
    if game.turn == 'X':
        coordinates = game.get_user_input()
        game.make_move('X', coordinates[0], coordinates[1])
        es.CLEAR()
        es.HOME()
        game.print_game_board(f"X played ({coordinates[0] + 1},{coordinates[1] + 1})")
    elif game.turn == 'O':
        ai_move = ai.make_Move(game)
        game.make_move('O', ai_move[0], ai_move[1])
        es.CLEAR()
        es.HOME()
        game.print_game_board(f"O played ({ai_move[0] + 1},{ai_move[1] + 1})")

    winner = game.check_for_winner(game.game_board)
    if game.tiles_taken == 9 and winner == False:
        run = False
        game.draw()
    elif winner:
        run = False
        print (f"{winner} has won the match!")
        game.print_game_board("Game over")
    if run == False:
        if play_again():
            run = True
            game.reset()
            es.CLEAR()
            es.HOME()

end_time = time.time()
log_file = open("logs.txt", "a")
log_file.write(f"Time Taken: {round(end_time-start_time, 5)}s\n")
log_file.close()