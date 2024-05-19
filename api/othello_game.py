class OthelloGame():

    def __init__(self, game_id : str, white_player : str, black_player : str):
        self.gameid = game_id
        self.white_player = white_player
        self.black_player = black_player
        self.board = [[0] * 8 for _ in range(8)]
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1

        self.current_player = -1
        self.score = {1: 2, -1 : 2}
        self.empty_squares = 60
        self.winner = None
        self.game_over = False
        self.strikes = {1 : 0, -1 : 0}
        self.last_move = {1 : 0 , -1 : 0}

    def display_board(self):
        for row in self.board:
            print('|'.join(map(str, row)))
            print('-' * 15)
    def is_valid_move(self, player, row, col):
        return (self.board[row][col] == 0)


    def update_board(self, player, row, col) -> bool:
        self.board[row][col] = self.current_player
        self.score[self.current_player] += 1
        self.empty_squares -= 1

        if self.current_player == -1:
            self.current_player = 1
        else:
            self.current_player = -1

        self.check_game_over()
        return True

    def check_game_over(self) -> bool:

        if self.empty_squares == 0:
            self.game_over = True
            if self.score[1] > self.score[-1]:
                self.winner = self.white_player
            if self.score[-1] > self.score[1]:
                self.winner = self.black_player
            if self.score[-1] == self.score[1]:
                self.winner = 'Tie'
            return True

        for row in self.board:
            if 0 in row:
                return False


        self.game_over = True
        if self.score[1] > self.score[-1]:
            self.winner = self.white_player
        if self.score[-1] > self.score[1]:
            self.winner = self.black_player
        if self.score[-1] == self.score[1]:
            self.winner = 'Tie'
        return True


if __name__ == '__main__':
    game = OthelloGame('test_game')
    game.display_board()
    game.update_board(game.current_player, 5,5)
    print('Move 1')
    game.display_board()
