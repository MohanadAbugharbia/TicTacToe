import pygame
import socket
import os
from threading import Thread
from base_game.base_game import Base_Game
from base_game.protocols import Socket_Protocol

class Client(Base_Game):
	def __init__(self, sock: Socket_Protocol) -> None:
		self.sock = sock

		self.turn = False
		self.player = ' '

		self.x_actual = 600
		self.y_actual = 600

		self.size = (self.x_actual, self.y_actual)

		self.grid_lines_width: int = 2

		self.x_grid = 400
		self.y_grid = 400
		
		self.x_difference = self.x_actual - self.x_grid
		self.y_difference = self.y_actual - self.y_grid

		self.board_start_x = (self.x_difference / 2) + self.grid_lines_width
		self.board_end_x = self.x_grid + (self.x_difference / 2) - self.grid_lines_width

		self.board_start_y = self.y_difference + self.grid_lines_width
		self.board_end_y = self.y_actual - self.grid_lines_width

		self.grid_lines = [
			((self.board_start_x, self.board_start_y), (self.board_end_x, self.board_start_y)),
			((self.board_start_x, self.board_start_y + (self.y_grid / 3)), (self.board_end_x, self.board_start_y + (self.y_grid / 3))),
			((self.board_start_x, self.board_start_y + (self.y_grid * 2 / 3)), (self.board_end_x, self.board_start_y + (self.y_grid * 2 / 3))),
			((self.board_start_x, self.board_end_y), (self.board_end_x, self.board_end_y)),

			((self.board_start_x, self.board_start_y), (self.board_start_x , self.board_end_y)),
			((self.board_start_x + self.x_grid / 3, self.board_start_y), (self.board_start_x  + self.x_grid / 3, self.board_end_y)),
			((self.board_start_x + self.x_grid / 1.5, self.board_start_y), (self.board_start_x  + self.x_grid * 2 / 3, self.board_end_y)),
			((self.board_end_x, self.board_start_y), (self.board_end_x, self.board_end_y)),
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
		self._game_board = [[" " for _ in range(3)] for _ in range(3)]

		self.black    = pygame.Color(   0,   0,   0)
		self.white    = pygame.Color( 255, 255, 255)
		self.green    = pygame.Color(   0, 255,   0)
		self.red      = pygame.Color( 255,   0,   0)
		self.blue	  = pygame.Color(   0,   0, 255)

	def start_gui(self) -> None:
		
		clock=pygame.time.Clock()
		while True:
			clock.tick(20)
			self.draw()
			pygame.display.flip()

	def start(self):
		game_start_info = self.sock.recv(1024).decode()
		self.game_state = "keepplaying"
		if game_start_info == "True":
			self.turn = "True"
			self.player = "X"
		else:
			self.turn = "False"
			self.player = "O"


		self.create_thread(self.receive_data, [])

		pygame.init()
		os.environ['SDL_VIDEO_WINDOW_POS'] = '650, 250'
		self.surface = pygame.display.set_mode(self.size)
		pygame.display.set_caption(f'Tic-tac-toe')

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
						if self.is_click_on_board(pos) is True:
							[x, y] = self.get_grid_coordinates_from_mouse_pos(pos)
							if self.get_mouse(x, y, self.player):
								send_data = '{}-{}-{}'.format(y, x, self.player).encode()
								self.sock.send(send_data)
								self.turn = "False"
							else:
								print("tile taken")
			clock.tick(20)
			self.draw()
			pygame.display.flip()

	def get_grid_coordinates_from_mouse_pos(self, pos: tuple[int, int]) -> list[int]:
		"""
			Returns the grid coordinates from the mouse position
			:param pos: the mouse position
			:return: the grid coordinates
		"""
		
		if self.is_click_on_board(pos) is False:
			raise Exception("Mouse click is not on the board.")
		
		x_grid_coordinate = int((pos[0] - self.board_start_x) // (self.x_grid / 3))
		y_grid_coordinate = int((pos[1] - self.board_start_y) // (self.y_grid / 3))

		return [x_grid_coordinate, y_grid_coordinate]


	def is_click_on_board(self, pos: tuple[int, int]) -> bool:
		"""
			Checks if the mouse click is on the board
			:param pos: the mouse position
			:return: True if the mouse click is on the board, False otherwise#
		"""
		x: int = pos[0]
		y: int = pos[1]

		x_on_board = True if x > self.board_start_x and x < self.board_end_x else False
		y_on_board = True if y > self.board_start_y and y < self.board_end_y else False

		return x_on_board and y_on_board
	
	def draw_game_details(self) -> None:
		self.surface.fill(self.white)
		text: str = f"Player: {self.player}"
		x: int = int(self.board_start_x + self.x_grid/3)
		y: int = 10
		self.add_text(text, self.black, [x, y])

		text: str = "Score"
		x: int = int(self.board_start_x + self.x_grid/3)
		y: int = 50
		self.add_text(text, self.black, [x, y])

		text: str = f"X : {self.num_of_wins['X']}"
		x: int = self.board_start_x
		y: int = 100
		self.add_text(text, self.red, [x, y])

		text: str = f"O : {self.num_of_wins['O']}"
		x: int = int(self.board_start_x + self.x_grid*2/3)
		y: int = 100
		self.add_text(text, self.red, [x, y])

	def draw_game_board(self) -> None:
		for y in range(len(self._game_board)):
			for x in range(len(self._game_board[y])):
				grid_coordinates: tuple[int, int] = (x, y)
				if self.get_cell_value(x, y) == "X":
					self.drawX(self.red, grid_coordinates)
				elif self.get_cell_value(x, y) == "O":
					self.drawO(self.red, grid_coordinates)

	def draw(self) -> None:
		
		self.draw_game_details()
		self.draw_grid()
		self.draw_game_board()

	def draw_grid(self):
		for line in self.grid_lines:
			pygame.draw.line(self.surface, self.black, line[0], line[1], self.grid_lines_width)

	def drawX(self, color: pygame.Color, grid_coordinates: tuple[int, int]) -> None:
		"""
			Draws an X on the board
			:param color: the color of the X
			:param grid_coordinates: the grid coordinates of the X
		:return: None
		"""

		x: int = grid_coordinates[0]
		y: int = grid_coordinates[1]
		x_start_coor: int = int(x*(self.x_grid/3) + self.board_start_x)
		x_end_coor: int = int(x*(self.x_grid/3) + self.board_start_x + (self.x_grid/3))
		y_start_coor: int = int(y*(self.y_grid/3) + self.board_start_y)
		y_end_coor: int = int(y*(self.y_grid/3) + self.board_start_y + (self.y_grid/3))
		width: int = 2

		pygame.draw.line(self.surface, color, (x_start_coor, y_start_coor), (x_end_coor, y_end_coor), width)
		pygame.draw.line(self.surface, color, (x_end_coor, y_start_coor), (x_start_coor, y_end_coor), width)
		
	def drawO(self, color: pygame.Color, grid_coordinates: tuple[int,int]) -> None:
		"""
			Draws an O on the board
			:param color: the color of the O
			:param grid_coordinates: the grid coordinates of the O
			:return: None
		"""

		radius: float = (self.x_grid / 3) / 2
		width: int = 2

		grid_x: int = grid_coordinates[0]
		grid_y: int = grid_coordinates[1]

		x_center: int = int(grid_x*(self.x_grid/3) + self.board_start_x + self.x_grid/6)
		y_center: int = int(grid_y*(self.y_grid/3) + self.board_start_y + self.y_grid/6)

		center: tuple[int, int] = (x_center, y_center)

		pygame.draw.circle(self.surface, color, center, radius, width)

	def get_cell_value(self, x: int, y: int) -> str:
		return self._game_board[x][y]

	def set_cell_value(self, x: int, y: int, value: str) -> None:
		self._game_board[x][y] = value

	def get_mouse(self, x: int, y: int, player: str) -> bool:
		if self.get_cell_value(x, y) != " ":
			return False
		if player in ['X', 'O']:
			self.set_cell_value(x, y, player)
		else:
			raise Exception(f"'{player}' can not play the game.")
		return True
		
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

	def add_text(self, text: str, color: pygame.Color, coordinates: list[int]) -> None:
		font = pygame.font.Font(None, 25)
		text = font.render(text, True, color)
		self.surface.blit(text, coordinates)


if __name__ == "__main__":
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

		host = '127.0.0.1'
		port = 5555

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		print("Connected to server")
		client = Client(sock)
		client.start()
