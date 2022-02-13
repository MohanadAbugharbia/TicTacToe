from game import Game
from computer import computer_Player
from escapesequences import escapesequences


game = Game()
computer = computer_Player()
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

game.print_game_board("Welcome to Tic-Tac-Toe\nYou are player X\n")
run = True
while run:
    if game.turn == 'X':
        coordinates = game.get_user_input()
        game.make_move('X', coordinates[0], coordinates[1])
        es.CLEAR()
        es.HOME()
        game.print_game_board(f"X played ({coordinates[0] + 1},{coordinates[1] + 1})")
    elif game.turn == 'O':
        computer_move = computer.make_Move(game)
        game.make_move('O', computer_move[0], computer_move[1])
        es.CLEAR()
        es.HOME()
        game.print_game_board(f"O played ({computer_move[0] + 1},{computer_move[1] + 1})")

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
            game.print_game_board("Welcome to Tic-Tac-Toe\nYou are player X\n")
