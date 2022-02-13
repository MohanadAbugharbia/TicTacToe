import random

random_choice = random.choice("XO")

def check_for_winner():
	game_has_been_won = False
	winner = ""
	if game_board[0][0] == game_board[1][1] == game_board[2][2] != " ":
		print("Congratulations")
		game_has_been_won = True
		winner = game_board[0][0]
	if game_board[0][2] == game_board[1][1] == game_board[2][0] != " ":
		print("Congratulations")
		game_has_been_won = True
		winner = game_board[0][2]
	for x in range(3):
		if game_board[x][0] == game_board[x][1] == game_board[x][2] != " ":
			print("Congratulations")
			game_has_been_won= True
			winner = game_board[x][0]
			break
		if game_board[0][x] == game_board[1][x] == game_board[2][x] != " ":
			print("Congratulations")
			game_has_been_won= True
			winner = game_board[0][x]
			break
	if game_has_been_won == True:
		print (f"{winner} has won the match!")
		return  winner
def check_winning_rules():
	check_winner_var = check_for_winner()
	if check_winner_var == "X" or check_winner_var == "O":
		return check_winner_var
	else:
		return False
def draw():
    print(f"The game has come to a draw.")
def is_tile_taken(x, y):
    if game_board[x][y] == "X" or game_board[x][y] == "O":
        return True
    else:
        return False
def print_game_board(text):
    print(text)
    print("Game board: ")
    for row in game_board:
        print(row)
game_board = [[" " for i in range(3)] for j in range(3)]

ruling = check_winning_rules()
tiles_taken = 0

while ruling == False:
    if tiles_taken != 9:
        while True:
            random_x = random.randint(0,2)
            random_y = random.randint(0,2)
            if is_tile_taken(random_x, random_y) == False:
                break
        game_board[random_x][random_y] = "X"
        tiles_taken += 1
        if tiles_taken == 9:
            break
        print_game_board(f"X played ({random_x + 1},{random_y + 1})")
        ruling = check_winning_rules()
        if ruling != False:
            break
        while True:
            x = int(input("Please choose a row: ")) -1
            y = int(input("Please choose a column: ")) - 1
            if is_tile_taken(x,y) == False:
                break
        game_board[x][y] = "O"
        tiles_taken += 1
        print_game_board(f"O played ({x + 1},{y + 1})")
    ruling = check_winning_rules()

if ruling == False:
    draw()
else:
    print_game_board("Game has been won")
