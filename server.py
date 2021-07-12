import socket
import threading

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

def create_thread(target):
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()


host = '127.0.0.1'
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(2)

print("Game is ready to be connected to")

def game_start(conn1, conn2):
	p1_info = '{}'.format("True").encode()
	p2_info = '{}'.format("False").encode()

	conn1.send(p1_info)
	conn2.send(p2_info)

def write_onto_the_game_board(x, y, player):
	if game_board[x][y] == " ":
		game_board[x][y] = player
		return True


def send_data_AND_await_response(connection, x, y, player):
	command = f"{x}-{y}-True-{player}-keepplaying".encode() # x, y, True, yourturn, player
	connection.send(command)
	return connection.recv(1024).decode()


def receive_data(conn1, conn2):
	data = conn1.recv(1024).decode()
	tiles_taken = 0
	while True:
		data = data.split('-') # x, y, player
		x = int(data[0])
		y = int(data[1])
		player = str(data[2])

		write_onto_the_game_board(int(data[0]), int(data[1]), player)
		tiles_taken += 1
		print(game_board)
		ruling = check_winning_rules()
		if ruling == 'X' or ruling == 'O':
				print(ruling)
				command = f"{x}-{y}-True-{player}-gameover".encode()
				conn1.send(command)
				conn2.send(command)
				break
		if tiles_taken != 9:
			if player == "X":
				data = send_data_AND_await_response(conn2, x, y, player)
			else:
				data = send_data_AND_await_response(conn1, x, y, player)
		elif ruling == False:
			command = f"{x}-{y}-True-{player}-draw".encode()
			conn1.send(command)
			conn2.send(command)
			print("Draw")
			break
		
		
	conn1.close()
	conn2.close()
	print("Clients disconnected")

def waiting_for_connection():
	conn1, addr1 = sock.accept()
	print(f"client is connected {addr1[0]} : {addr1[1]}")
	conn2, addr2 = sock.accept()
	print(f"client is connected {addr2[0]} : {addr2[1]}")
	connection_established = True
	game_start(conn1, conn2)
	receive_data(conn1, conn2)


create_thread(waiting_for_connection)

game_board = [[" " for i in range(3)] for j in range(3)]
while True:
	pass