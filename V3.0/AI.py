import random
from turtle import pos
from game import Game

class AI:
	def __init__(self):
		self.game_board2 = [1,2,3]
	
	def make_Move(self, game):
		# [['0', '1', '2'],
		#  ['3', '4', '5'],
		#  ['6', '7', '8']]
		game_board = game.get_game_board()
		board = self.generate_AI_board(game_board)
		possible_moves = [x for x, letter in enumerate(board) if letter == ' ']
		move = 0

		for let in ['O', 'X']:
			for i in possible_moves:
				board_copy = board[:]
				board_copy[i] = let
				if game.check_for_winner(self.generate_game_board(board_copy)):
					move = i
					return self.move_to_coordinates(move)
		cornersOpen = []
		#check for open corners
		for i in possible_moves:
			if i in [0,2,6,8]:
				cornersOpen.append(i)
		if len(cornersOpen) > 0:
			move = self.selectRandom(cornersOpen)
			return self.move_to_coordinates(move)

		#check if center is open
		if 4 in possible_moves:
			move = 4
			return self.move_to_coordinates(move)
		
		edgesOpen = []
		#check for open edges
		for i in possible_moves:
			if i in [1,3,5,7]:
				edgesOpen.append(i)
		if len(edgesOpen) > 0:
			move = self.selectRandom(edgesOpen)
			return self.move_to_coordinates(move)
	def selectRandom(self, li):
		ln = len(li)
		r = random.randrange(0, ln)
		return li[r]

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
	def generate_AI_board(self, old_board):
		new_board = []
		for i in old_board:
			for j in i:
				new_board.append(j)
		return new_board

	def generate_game_board(self, old_board):
		new_board = [[' ' for i in range(3)] for j in range(3)]
		for i in range(3):
			for j in range(3):
				if i != 0:
					new_board[i][j] = old_board[(i*3)+j]
				else:
					new_board[i][j] = old_board[j]
		return new_board