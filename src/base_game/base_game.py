


class Base_Game:
    def __init__(self) -> None:
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]
        self.winner = ' '
        
    def check_winner(self) -> str:
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] != " ":
            self.winner = self.game_board[0][0]
        elif self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != " ":
            self.winner = self.game_board[0][2]
        else:
            for x in range(3):
                if self.game_board[x][0] == self.game_board[x][1] == self.game_board[x][2] != " ":
                    self.winner = self.game_board[x][0]
                    break
                elif self.game_board[0][x] == self.game_board[1][x] == self.game_board[2][x] != " ":
                    self.winner = self.game_board[0][x]
                    break
        return self.winner


    def get_winner(self) -> str:
        if self.winner == ' ':
            return self.check_winner()
        else:
            return self.winner