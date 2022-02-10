import pygame


class Game:
    def __init__(self):
        self.game_board = [[' ' for i in range(3)] for j in range(3)]
        self.tiles_taken = 0
        self.turn = 'X'
        self.grid_lines = [
                            ((  0, 200), (  0, 600)),
                            ((399, 200), (399, 600)),
                            ((  0, 598), (400, 598)),
                            ((  0, 200), (400, 200)), #first horizontal line
                            ((  0, 333), (400, 333)), #second horizontal line
                            ((  0, 466), (400, 466)), #third horizontal line
                            ((133, 200), (133, 600)), #first vertical line
                            ((266, 200), (266, 600))] #second vertical line
        size = (400, 600)
        print(f"size: {size[0]}, {size[1]}")
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(f'Tic-tac-toe player X')

    def draw(self):
        red_color = (255, 0, 0)
        black_color = (0, 0, 0)
        white_color = (255, 255, 255)
        self.surface.fill(white_color)

        for line in self.grid_lines:
            pygame.draw.line(self.surface, black_color, line[0], line[1], 3)

        for y in range(len(self.game_board)):
            for x in range(len(self.game_board[y])):
                if self.get_cell_value(x, y) == "X":
                    pygame.draw.line(self.surface, red_color, (x*133, y*133 + 200), (x*133 + 133, y*133 + 333), 3)
                    pygame.draw.line(self.surface, red_color, (x*133 + 133, y*133+ 200), (x*133, y*133 + 333), 3)

                elif self.get_cell_value(x, y) == "O":
                    pygame.draw.circle(self.surface, red_color, (x*133 + 66, y*133 + 266), 66, 3)

    def get_cell_value(self, x, y):
        return self.game_board[x][y]

    def get_mouse(self, x, y):
        if self.get_cell_value(x, y) == ' ':
            return True
        else:
            return False

    def check_for_winner(self, board):
        winner = ' '
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            winner = board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            winner = board[0][2]
        for x in range(3):
            if board[x][0] == board[x][1] == board[x][2] != ' ':
                winner = board[x][0]
                break
            if board[0][x] == board[1][x] == board[2][x] != ' ':
                winner = board[0][x]
                break
        if winner != ' ':
            return  winner
        else:
            return False

    def get_user_input(self):
        while True:
            while True:
                x = input("Please choose a row to place an X (1-3): ")
                try:
                    x = int(x) - 1
                    if x >= 0 and x < 3:
                        break
                    else:
                        print('Please type a number within the range!')
                except:
                    print('Please type a number!')
            while True:
                y = input("Please choose a column to place an X (1-3): ")
                try:
                    y = int(y) - 1
                    if y >= 0 and y < 3:
                        break
                    else:
                        print('Please type a number within the range!')
                except:
                    print('Please type a number!')
            if not self.is_tile_taken(x,y):
                break
        return x, y

    def no_winner_draw(self):
        print(f"The game has come to a draw.")

    def is_tile_taken(self, x, y):
        if self.game_board[x][y] == ' ':
            return False
        else:
            return True
    
    def make_move(self, x, y, player):
        self.game_board[x][y] = player
        self.tiles_taken += 1
        if player == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def print_game_board(self, text):
        print(text)
        print("Game board: ")
        print("=================================")
        for row in self.game_board:
            for letter in row:
                print(f"|   {letter}     |", end="")
            print("\n---------------------------------")
            

    def get_game_board(self):
        return self.game_board
    
    def reset(self):
        self.tiles_taken = 0
        self.game_board = [[' ' for i in range(3)] for j in range(3)]
        self.turn = 'X'