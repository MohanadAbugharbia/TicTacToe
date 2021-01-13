import socket
import threading
#from _thread import *
def check_winner():
	won = False
	winner = ""
	if gameTable[0][0] == gameTable[1][1] == gameTable[2][2] != " ":
		print("Congratulations")
		won = True
		winner = gameTable[0][0]
	if gameTable[0][2] == gameTable[1][1] == gameTable[2][0] != " ":
		print("Congratulations")
		won = True
		winner = gameTable[0][2]
	for x in range(3):
		if gameTable[x][0] == gameTable[x][1] == gameTable[x][2] != " ":
			print("Congratulations")
			won= True
			winner = gameTable[x][0]
			break
		if gameTable[0][x] == gameTable[1][x] == gameTable[2][x] != " ":
			print("Congratulations")
			won= True
			winner = gameTable[0][x]
			break
	if winner == "X":
		winning_Player = "Player 1"
	else:
		winning_Player = "Player 2"
	
	if won == True:
		print (winning_Player + " has won the match!")
		return  winner

def rules(tiles_taken):
	check_winner_var = check_winner()
	if check_winner_var == "X" or "O":
		return check_winner_var
	else:
		return False

def create_thread(target):
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()


#host = '167.172.156.226'
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

def check_input(x, y, player):
	if gameTable[x][y] == " ":
		gameTable[x][y] = player
		return True

def receive_data(conn1, conn2):
	data = conn1.recv(1024).decode()
	tiles_taken = 0
	while True:
		data = data.split('-') # x, y, player
		player = str(data[2])
		check_input(int(data[0]), int(data[1]), player)
		tiles_taken += 1
		print(tiles_taken)
		print(gameTable)
		ruling = rules(tiles_taken)
		if tiles_taken != 9:
			if ruling != False and ruling != None:
				print(ruling)
				command = '{}-{}-{}-{}-{}'.format(data[0], data[1], "True", player, "gameover").encode()
				conn1.send(command)
				conn2.send(command)
				break
			if player == "X":
				command = '{}-{}-{}-{}-{}'.format(data[0], data[1], "True", player, "keepplaying").encode() # x, y, True, yourturn, player
				conn2.send(command)
				data = conn2.recv(1024).decode()
			else:
				command = '{}-{}-{}-{}-{}'.format(data[0], data[1], "True", player, "keepplaying").encode() # x, y, True, yourturn, player
				conn1.send(command)
				data = conn1.recv(1024).decode()
		else:
			command = '{}-{}-{}-{}-{}'.format(data[0], data[1], "True", player, "draw").encode()
			conn1.send(command)
			conn2.send(command)
			print("Draw")
			break
		
		
	conn1.close()
	conn2.close()
	print("Clients disconnected")

	

def waiting_for_connection():
	conn1, addr1 = sock.accept()
	print("Client is connected " + str(addr1[0]) + ":" + str(addr1[1]))
	conn2, addr2 = sock.accept()
	print("Client is connected " + str(addr2[0]) + ":" + str(addr2[1]))
	connection_established = True
	game_start(conn1, conn2)
	receive_data(conn1, conn2)


create_thread(waiting_for_connection)

gameTable = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
while True:
	pass