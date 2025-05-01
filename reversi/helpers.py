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
