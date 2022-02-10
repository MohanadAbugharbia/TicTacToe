import pygame
import os
import socket
import threading
from grid import Grid

def create_thread(target):
	thread = threading.Thread(target = target)
	thread.daemon = True
	thread.start()

os.environ['SDL_VIDEO_WINDOW_POS'] = '650, 250'
size = (400, 600)
surface = pygame.display.set_mode(size)
pygame.display.set_caption('Tic-tac-toe')
grid = Grid()

host = '127.0.0.1'
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
print("Connected to server")

game_start_info = sock.recv(1024).decode()
game_start_info = game_start_info.split('-')
if game_start_info[0] == "True":
	turn = "True"
	player = "X"
else:
	turn = "False"
	player = "O"

print(f"I am player: {player}")
pygame.display.set_caption(f'Tic-tac-toe player {player}')

def receive_data():
	global turn, running
	while True:
		data = sock.recv(2048).decode()    # x, y, turn, player, game_state
		data = data.split('-')
		x_Position = int(data[0])
		y_Position = int(data[1])
		turn = str(data[2])
		player = data[3]
		game_state = data[4]
		grid.get_mouse(y_Position, x_Position, player)
		if game_state == "gameover":
			print(f"Good game, player {player} has won the game.")
			break
		if game_state == "draw":
			print("The game comes to a draw")
			break

create_thread(receive_data)


running = True
clock=pygame.time.Clock()

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if turn == "True":
					pos = pygame.mouse.get_pos()
					if pos[1] >= 200:
						if grid.get_mouse(pos[0] // 133, (pos[1] - 200) // 133, player):
							send_data = '{}-{}-{}'.format((pos[1] - 200) // 133, pos[0] // 133, player).encode()
							sock.send(send_data)
							turn = "False"
						else:
							print("tile taken")
	clock.tick(20)
	grid.draw(surface)
	pygame.display.flip()