

class Game:
    def __init__(self):
        self.game_board = [[' ' for i in range(3)] for j in range(3)]
        self.tiles_taken = 0
        self.turn = 'X'
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

    def draw(self):
        print(f"The game has come to a draw.")

    def is_tile_taken(self, x, y):
        if self.game_board[x][y] == "X" or self.game_board[x][y] == "O":
            return True
        else:
            return False
    
    def make_move(self, player, x, y):
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