from game import take_turn

def expectimax_player(game_state, depth):
    if depth == 0:
        return game_state.score, None
    best_score = 0
    best_move = None
    for move in ['up', 'down', 'left', 'right']:
        new_state = game_state.copy()
        take_turn(new_state, move)
        score = expectimax_chance(new_state, depth - 1)
        if score > best_score:
            best_score = score
            best_move = move
    return best_score, best_move

def expectimax_chance(game_state, depth):
    if depth == 0:
        return game_state.score
    empty_squares = []
    for i in range(4):
        for j in range(4):
            if game_state.board[i][j] == 0:
                empty_squares.append((i, j))
    total_score = 0
    for i, j in empty_squares:
        new_state = game_state.copy()
        new_state.board[i][j] = 2
        score = expectimax_player(new_state, depth - 1)[0]
        total_score += score * 0.9 / len(empty_squares)
    for i, j in empty_squares:
        new_state = game_state.copy()
        new_state.board[i][j] = 4
        score = expectimax_player(new_state, depth - 1)[0]
        total_score += score * 0.1 / len(empty_squares)
    return total_score