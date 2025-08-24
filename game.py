import random

class GameState:
    def __init__(self, board, score):
        self.board = board
        self.score = score
    
    def copy(self):
        return GameState([row[:] for row in self.board], self.score)
    
# populates board with 2 or 4
def new_game_tile(board):
    no_space = True
    while any(0 in row for row in board):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        if board[x][y] == 0:
            if random.randint(1, 10) == 10:
                board[x][y] = 4
            else:
                board[x][y] = 2
            no_space = False
            break
    return board, no_space

# takes turn and moves tiles
def take_turn(state, orientation):
    board = state.board
    merged = [[False for _ in range(4)] for _ in range(4)]
    if orientation == 'down':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        state.score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif orientation == 'up':
        for i in range(4):
            for j in range(4):
                shift = 0 
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board [i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] and not merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        state.score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    elif orientation == 'left':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift - 1] == board[i][j - shift] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    state.score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
    elif orientation == 'right':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        state.score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True