import socket
from threading import Thread

class game_session:
	def __init__(self, player1: socket.socket, player2: socket.socket):
		self.game_board = [[" " for i in range(3)] for j in range(3)]
		self.player1 = player1
		self.player2 = player2
		self.winner = ' '

		player1.send('True'.encode())
		player2.send('False'.encode())

		data = player1.recv(1024).decode()
		tiles_taken = 0
		while True:
			data = data.split('-') # x, y, player
			x_pos = int(data[0])
			y_pos = int(data[1])
			turn = str(data[2])
			self.write_to_game_board(x_pos, y_pos, turn)
			print(self.game_board)
			ruling = self.get_winner()
			if ruling == 'X' or ruling == 'O':
					print(ruling)
					message = f"{x_pos}-{y_pos}-True-{turn}-gameover".encode()
					player1.send(message)
					player2.send(message)
					break
			if tiles_taken != 9:
				if turn == "X":
					data = self.send_data_AND_wait_for_response(player2, x_pos, y_pos, turn)
				else:
					data = self.send_data_AND_wait_for_response(player1, x_pos, y_pos, turn)
				tiles_taken += 1
			elif ruling == False:
				message = f"{x_pos}-{y_pos}-True-{turn}-draw".encode()
				player1.send(message)
				player2.send(message)
				break
			
		player1.close()
		player2.close()
		print("Clients disconnected")

	def check_winner(self) -> str:
		if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] != " ":
			self.winner = self.game_board[0][0]
		elif self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != " ":
			self.winner = self.game_board[0][2]
		else:
			for x in range(3):
				if self.game_board[x][0] == self.game_board[x][1] == self.game_board[x][2] != " ":
					self.winner = self.game_board[x][0]
					break
				elif self.game_board[0][x] == self.game_board[1][x] == self.game_board[2][x] != " ":
					self.winner = self.game_board[0][x]
					break
		return self.winner


	def get_winner(self) -> str:
		if self.winner != ' ':
			return self.check_winner()
		else:
			return self.winner


	def write_to_game_board(self, x: int, y: int, player: chr) -> None:
		if self.game_board[x][y] == " ":
			self.game_board[x][y] = player

	def send_data_AND_wait_for_response(self, player: socket.socket, x: int, y: int, turn: str) -> str:
		message = f"{x}-{y}-True-{turn}-keepplaying".encode()
		player.send(message)
		return player.recv(1024).decode()

		


def create_thread(target, args) -> Thread:
	thread = Thread(target = target, args=args)
	thread.daemon = True
	thread.start()
	return thread

def start_session(player1: socket.socket, player2: socket.socket) -> Thread:
	return create_thread(game_session, [player1, player2])

if __name__ == "__main__":

	host = '127.0.0.1'
	port = 5555
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

		sock.bind((host, port))
		sock.listen(2)

		print("Game is ready to be connected to")

		while True:
			player1, addr1 = sock.accept()
			print(f"Player1 is connected {addr1[0]} : {addr1[1]}")
			player2, addr2 = sock.accept()
			print(f"Player2 is connected {addr2[0]} : {addr2[1]}")
			start_session(player1, player2)