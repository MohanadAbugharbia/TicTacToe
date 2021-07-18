import socket
import threading
import time

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
	if winner == "X":
		winning_Player = "Player 1"
	else:
		winning_Player = "Player 2"
	
	if game_has_been_won == True:
		print (f"{winning_Player} has won the match!")
		return  winner

def check_winning_rules():
	check_winner_var = check_for_winner()
	if check_winner_var == "X" or "O":
		return check_winner_var
	else:
		return False


host = '127.0.0.1'
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(2)

print("Game is ready to be connected to")

def game_initialistaion(player1, player2):
	p1_info = 'True'.encode()
	p2_info = 'False'.encode()

	player1.send(p1_info)
	player2.send(p2_info)

def write_onto_the_game_board(x, y, player):
	if game_board[x][y] == " ":
		game_board[x][y] = player
		return True


def send_data_AND_wait_for_response(player, x, y, turn):
	message = f"{x}-{y}-True-{turn}-keepplaying".encode()
	player.send(message)
	return player.recv(1024).decode()


def game_start(player1, player2):
	data = player1.recv(1024).decode()
	tiles_taken = 0
	while True:
		data = data.split('-') # x, y, player
		x = int(data[0])
		y = int(data[1])
		turn = str(data[2])

		write_onto_the_game_board(x, y, turn)
		print(game_board)
		ruling = check_winning_rules()
		if ruling == 'X' or ruling == 'O':
				print(ruling)
				message = f"{x}-{y}-True-{turn}-gameover".encode()
				player1.send(message)
				player2.send(message)
				break
		if tiles_taken != 9:
			if turn == "X":
				data = send_data_AND_wait_for_response(player2, x, y, turn)
			else:
				data = send_data_AND_wait_for_response(player1, x, y, turn)
			tiles_taken += 1
		elif ruling == False:
			message = f"{x}-{y}-True-{turn}-draw".encode()
			player1.send(message)
			player2.send(message)
			print("Draw")
			break
		
		
	player1.close()
	player2.close()
	print("Clients disconnected")

def waiting_for_connection():
	player1, addr1 = sock.accept()
	print(f"Player1 is connected {addr1[0]} : {addr1[1]}")
	player2, addr2 = sock.accept()
	print(f"Player2 is connected {addr2[0]} : {addr2[1]}")
	connection_established = True
	game_initialistaion(player1, player2)
	game_start(player1, player2)


def create_thread(target):
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()

create_thread(waiting_for_connection)

game_board = [[" " for i in range(3)] for j in range(3)]
while True:
	time.sleep(100)