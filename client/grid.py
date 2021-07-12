import pygame
import os

class Grid:
	def __init__(self):
		self.grid_lines = [	((0, 225), (675, 225)), #first horizontal line
							((0, 450), (675, 450)), #second horizontal line
							((225, 0), (225, 675)), #first vertical line
							((450, 0), (450, 675))] #second vertical line
		self.grid = [[0 for x in range(3)] for y in range(3)]

	def draw(self, surface):
		red_color = (255, 0, 0)
		for line in self.grid_lines:
			pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

		for y in range(len(self.grid)):
			for x in range(len(self.grid[y])):
				if self.get_cell_value(x, y) == "X":
					#surface.blit(letterX, (x*225, y*225))
					pygame.draw.line(surface, red_color, (x*225, y*225), (x*225 + 225, y*225 + 225), 2)
					pygame.draw.line(surface, red_color, (x*225 + 225, y*225), (x*225, y*225 + 225), 2)

				elif self.get_cell_value(x, y) == "O":
					#surface.blit(letterO, (x*225, y*225))
					pygame.draw.circle(surface, red_color, (x*225 + 112, y*225 + 112), 112, 2)

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