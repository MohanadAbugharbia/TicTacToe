import pygame
import socket
import os
from base_game.base_game import Base_Game
from threading import Thread

class Client(Base_Game):
	def __init__(self, sock: socket.socket) -> None:
		self.sock = sock

		self.x_actual = 400
		self.y_actual = 600

		self.size = (self.x_actual, self.y_actual)
		
		self.x_grid = 400
		self.y_grid = 400
		
		self.x_difference = self.x_actual - self.x_grid
		self.y_difference = self.y_actual - self.y_grid

		self.grid_lines = [
			((self.x_difference, self.y_difference), (self.x_grid, self.y_difference)),
			((self.x_difference, self.y_difference + (self.y_grid / 3)), (self.x_grid, self.y_difference + (self.y_grid / 3))),
			((self.x_difference, self.y_difference + (self.y_grid / 1.5)), (self.x_grid, self.y_difference + (self.y_grid / 1.5))),

			((self.x_grid / 3, self.y_difference), (self.x_grid / 3, self.y_actual)),
			((self.x_grid / 1.5, self.y_difference), (self.x_grid / 1.5, self.y_actual))
		]
		self.num_of_wins = {
			"X" : 0,
			"O" : 0
		}
		# self.grid_lines = [
		# 					((  0, 200), (400, 200)), #first horizontal line
		# 					((  0, 333), (400, 333)), #second horizontal line
		# 					((  0, 466), (400, 466)), #third horizontal line
		# 					((133, 200), (133, 600)), #first vertical line
		# 					((266, 200), (266, 600))] #second vertical line
		self.game_board = [[" " for _ in range(3)] for _ in range(3)]

		self.black    = (   0,   0,   0)
		self.white    = ( 255, 255, 255)
		self.green    = (   0, 255,   0)
		self.red      = ( 255,   0,   0)
		self.blue	  = (   0,   0, 255)


		self.start()

	def start(self):
		pygame.init()
		os.environ['SDL_VIDEO_WINDOW_POS'] = '650, 250'

		game_start_info = self.sock.recv(1024).decode()
		self.game_state = "keepplaying"
		if game_start_info == "True":
			self.turn = "True"
			self.player = "X"
		else:
			self.turn = "False"
			self.player = "O"

		self.surface = pygame.display.set_mode(self.size)
		pygame.display.set_caption(f'Tic-tac-toe')


		self.create_thread(self.receive_data, [])


		running = True
		clock=pygame.time.Clock()

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif self.game_state != "keepplaying":
					continue
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.turn == "True":
						pos = pygame.mouse.get_pos()
						if pos[1] >= self.y_difference:
							if self.get_mouse(int((pos[0] - self.x_difference) // (self.x_grid / 3)), int((pos[1] - self.y_difference) // (self.y_grid / 3)), self.player):
								send_data = '{}-{}-{}'.format(int((pos[1] - self.y_difference) // (self.y_grid / 3)), int((pos[0] - self.x_difference) // (self.x_grid / 3)), self.player).encode()
								self.sock.send(send_data)
								self.turn = "False"
							else:
								print("tile taken")
			clock.tick(20)
			self.draw()
			pygame.display.flip()

	def draw(self) -> None:
		self.surface.fill(self.white)
		
		self.add_text(f"Player: {self.player}", self.black, [150, 10])
		self.add_text(f"Score", self.black, [150,50])
		self.add_text(f"X : {self.num_of_wins['X']}", self.red, [50, 100])
		self.add_text(f"O : {self.num_of_wins['O']}", self.red, [300, 100])

		self.draw_grid()

		for y in range(len(self.game_board)):
			for x in range(len(self.game_board[y])):
				if self.get_cell_value(x, y) == "X":
					pygame.draw.line(self.surface, self.red, (x*133, y*133 + 200), (x*133 + 133, y*133 + 333), 2)
					pygame.draw.line(self.surface, self.red, (x*133 + 133, y*133+ 200), (x*133, y*133 + 333), 2)

				elif self.get_cell_value(x, y) == "O":
					self.drawO(self.red, (x*133 + 66, y*133 + 266))

	def draw_grid(self):
		for line in self.grid_lines:
			pygame.draw.line(self.surface, self.black, line[0], line[1], 2)

	def drawO(self, color: tuple[int,int,int], coordinates: tuple[int,int]) -> None:
		radius: float = 66
		width: int = 2
		pygame.draw.circle(self.surface, color, coordinates, radius, width)

	def get_cell_value(self, x: int, y: int) -> chr:
		return self.game_board[x][y]

	def set_cell_value(self, x: int, y: int, value: chr) -> None:
		self.game_board[x][y] = value

	def get_mouse(self, x: int, y: int, player: chr) -> bool:
		if self.get_cell_value(x, y) == " ":
			if player == "X":
				self.set_cell_value(x, y, "X")
			elif player == "O":
				self.set_cell_value(x, y, "O")
			return True
		else:
			return False
			
	def create_thread(self, target, args) -> Thread:
		thread = Thread(target = target, args=args)
		thread.daemon = True
		thread.start()
		return thread

	def receive_data(self):
		while True:
			data = self.sock.recv(2048).decode()    # x, y, turn, player, game_state
			data = data.split('-')
			x_Position = int(data[0])
			y_Position = int(data[1])
			self.turn = str(data[2])
			player = data[3]
			self.game_state = data[4]
			self.get_mouse(y_Position, x_Position, player)
			if self.game_state == "gameover":
				print(f"Good game, player {player} has won the game.")
				self.num_of_wins[player] += 1
				break
			if self.game_state == "draw":
				print("The game comes to a draw")
				break

	def add_text(self, text: str, color: pygame.Color, coordinates: list[int, int]) -> None:
		font = pygame.font.Font(None, 25)
		text = font.render(text,True,color)
		self.surface.blit(text, coordinates)


if __name__ == "__main__":
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

		host = '127.0.0.1'
		port = 5555

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		print("Connected to server")
		client = Client(sock)
