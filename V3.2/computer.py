import random


class computer_Player:
	def __init__(self):
		self.game_board2 = [1,2,3]
	
	def generate_Move(self, game):
		#game_board = [['0', '1', '2'], 
		#			 ['3', '4', '5'],
		#			 ['6', '7', '8']]
		board = self.game_board_TO_board(game.game_board)
		#board = [' ', ' ' , ' ',
		#		 ' ', ' ', ' ', 
		#		 ' ', ' ', ' ' ]
		possible_moves = [x for x, letter in enumerate(board) if letter == ' ']

		for letter in ['O', 'X']:
			for i in possible_moves:
				board_copy = board[:]
				board_copy[i] = letter
				if game.check_for_winner(self.board_TO_game_board(board_copy)):
					move = i
					return self.move_to_coordinates(move)

		free_corners = []
		#check for open corners
		for i in possible_moves:
			if i in [0,2,6,8]:
				free_corners.append(i)
		if len(free_corners) > 0:
			move = self.select_random(free_corners)
			return self.move_to_coordinates(move)

		#check if center is open
		if 4 in possible_moves:
			move = 4
			return self.move_to_coordinates(move)
		
		free_edges = []
		#check for open edges
		for i in possible_moves:
			if i in [1,3,5,7]:
				free_edges.append(i)
		if len(free_edges) > 0:
			move = self.select_random(free_edges)
			return self.move_to_coordinates(move)

	
	def select_random(self, list):
		random_nr = random.randrange(0, len(list))
		return list[random_nr]

	def move_to_coordinates(self, move):
		if move == 0:
			return 0, 0
		if move == 1:
			return 0, 1
		if move == 2:
			return 0, 2
		if move == 3:
			return 1, 0
		if move == 4:
			return 1, 1
		if move == 5:
			return 1, 2
		if move == 6:
			return 2, 0
		if move == 7:
			return 2, 1
		if move == 8:
			return 2, 2

	def game_board_TO_board(self, old_board):
		new_board = []
		for i in old_board:
			for j in i:
				new_board.append(j)
		return new_board

	def board_TO_game_board(self, old_board):
		new_board = [[' ' for i in range(3)] for j in range(3)]
		for i in range(3):
			for j in range(3):
				if i != 0:
					new_board[i][j] = old_board[(i*2)+j+i]
				else:
					new_board[i][j] = old_board[j]
		return new_board