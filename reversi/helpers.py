from reversi.constants import ROWS, COLS
def is_corner(row, col):
    corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]
    move = row, col
    if move in corners:
        return True
    else:
        return False


def is_wall(row, col):
    if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
        return True
    else:
        return False

# a square is only dangerous if the corner is free
def dangerous_square(row, col,board):
    dangerous_squares = {
        # top left
        (0, 1): (0, 0),
        (1, 0): (0, 0),
        (1, 1): (0, 0),
        # top right
        (0, COLS - 2): (0, COLS - 1),
        (1, COLS - 2): (0, COLS - 1),
        (1, COLS - 1): (0, COLS - 1),
        # bottom left
        (ROWS - 2, 0): (ROWS - 1, 0),
        (ROWS - 2, 1): (ROWS - 1, 0),
        (ROWS - 1, 1): (ROWS - 1, 0),
        # bottom right
        (ROWS - 2, COLS - 2): (ROWS - 1, COLS - 1),
        (ROWS - 2, COLS - 1): (ROWS - 1, COLS - 1),
        (ROWS - 1, COLS - 2): (ROWS - 1, COLS - 1),
    }

    move = row, col
    if move in dangerous_squares:
        corner_row, corner_col = dangerous_squares.get(move)
        return board[corner_row][corner_col] == 0
    else:
        return False


def is_inside(row, col):
    if row in range(2, ROWS - 2) and col in range(2, COLS - 2):
        return True
    else:
        return False
def min_max_search(board,player,num):
    # get the biggest possible score after num moves
    # only interested in the move not the score
    move, _ = max_score(board,player,num)
    return move


def max_score(board, player, num):
    next_moves = board.next_moves()
    num -= 1 # we are one depth deeper
    if len(next_moves) == 0: #if no move are available
        return None, board.board_heuristic(player)# terminal state or pass

    best_move, best_move_score = None, float('-inf')
    for move in next_moves:
        row, col = move
        temp_board = board.copy()
        temp_board.make_move(row, col) # make move
        if num == 0: # this is our depth to test
            temp_score = temp_board.board_heuristic(player)
        else:
            _, temp_score = min_score(temp_board,player,num) # go deeper and get score
        if temp_score > best_move_score:
            best_move = move
            best_move_score = temp_score
    return best_move, best_move_score

def min_score(board,player,num):
    next_moves = board.next_moves()
    if len(next_moves) == 0:  # no moves ahead
        return None, board.board_heuristic(player) #change?
    num -= 1
    best_move, best_move_score = None, float('inf')
    for move in next_moves:
        row, col = move
        temp_board = board.copy()
        temp_board.make_move(row, col)  # make move
        if num == 0:
            temp_score = temp_board.board_heuristic(player)
        else:
            _, temp_score = max_score(temp_board, player, num)
        if temp_score < best_move_score:
            best_move = move
            best_move_score = temp_score
    return best_move, best_move_score
