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

surface = pygame.display.set_mode((675, 675))
pygame.display.set_caption('Tic-tac-toe')
grid = Grid()

running = True

#host = '18.185.172.166'
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

print("I am player: " + player)

def receive_data():
	global turn, running
	while True:
		data = sock.recv(2048).decode()    # x, y, True, yourturn, player
		data = data.split('-')
		grid.get_mouse(int(data[1]), int(data[0]), str(data[3]))
		if data[4] == "gameover":
			print("Good game, player " + data[3] + " has won the game.")

			break
		if data[4] == "draw":
			print("The game comes to a draw")
			break
		turn = str(data[2])

create_thread(receive_data)
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if turn == "True":
					pos = pygame.mouse.get_pos()
					if grid.get_mouse(pos[0] // 225, pos[1] // 225, player):
						send_data = '{}-{}-{}'.format(pos[1] // 225, pos[0] // 225, player).encode()
						sock.send(send_data)
						turn = "False"
					else:
						print("tile taken")
	surface.fill((0,0,0))
	grid.draw(surface)
	pygame.display.flip()