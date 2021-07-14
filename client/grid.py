import pygame
import os

class Grid:
	def __init__(self):
		self.grid_lines = [
							((  0, 200), (400, 200)), #first horizontal line
							((  0, 333), (400, 333)), #second horizontal line
							((  0, 466), (400, 466)), #third horizontal line
							((133, 200), (133, 600)), #first vertical line
							((266, 200), (266, 600))] #second vertical line
		self.grid = [[0 for x in range(3)] for y in range(3)]

	def draw(self, surface):
		red_color = (255, 0, 0)
		black_color = (0, 0, 0)
		white_color = (255, 255, 255)
		surface.fill(white_color)
		
		for line in self.grid_lines:
			pygame.draw.line(surface, black_color, line[0], line[1], 2)

		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.get_cell_value(x, y) == "X":
					pygame.draw.line(surface, red_color, (x*133, y*133 + 200), (x*133 + 133, y*133 + 333), 2)
					pygame.draw.line(surface, red_color, (x*133 + 133, y*133+ 200), (x*133, y*133 + 333), 2)

				elif self.get_cell_value(x, y) == "O":
					pygame.draw.circle(surface, red_color, (x*133 + 66, y*133 + 266), 66, 2)

	def get_cell_value(self, x, y):
		return self.grid[y][x]

	def set_cell_value(self, x, y, value):
		self.grid[y][x] = value

	def get_mouse(self, x, y, player):
		if self.get_cell_value(x, y) == 0:
			if player == "X":
				self.set_cell_value(x, y, "X")
			elif player == "O":
				self.set_cell_value(x, y, "O")
			return True