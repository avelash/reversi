
import pygame
import copy
from reversi.constants import *
from reversi.helpers import is_corner, dangerous_square, is_wall, is_inside
from reversi.piece import Piece




# class board defines a board for a reversi game
# we could have created a generic board and in a different class used it for the game.
# choose this way to keep number of files minimal for the assignment.
class Board:
    moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def __init__(self):
        self.board = []
        self.black_pieces = self.white_pieces = 2
        self.turn = WHITE #white starts
        self.turns_played = 0
        self.create_board() #init board with the standard opening position.


    #for printing the current state of the board
    def __repr__(self):
        board_str = f"state: {self.turns_played}\n"
        for row in range(ROWS):
            for col in range(COLS):
                board_str += f'{str(self.board[row][col])} '
            board_str += '\n'
        return  board_str

    def copy(self):
        return copy.deepcopy(self)

    # init board with the standard opening position.
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                #places for starting white pieces are middle top left and middle bottom right
                if (row == ROWS // 2 - 1 and col == COLS // 2 - 1) or (row == ROWS // 2 and col == COLS // 2):
                    self.board[row].append(Piece(row, col, WHITE))
                    # places for starting black pieces are middle top right and middle bottom left
                elif (row == ROWS // 2 - 1 and col == COLS // 2) or (row == ROWS // 2 and col == COLS // 2 - 1):
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0) #0 represents an empty square

    #drawing board with pygame
    def draw_board(self,win):
        win.fill(GREEN)
        for i in range(1, ROWS):
            pygame.draw.line(win, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 2)
            pygame.draw.line(win, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 2)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    #check if a move is legal
    def is_legal(self, row, col):
        if self.board[row][col] != 0:
            return False # square is not empty
        opponent = self.get_opponent()
        for row_move, col_move in self.moves:
            row_check, col_check = row + row_move, col + col_move # check square in "move" direction.
            found_opponent = False #for a move to be legal we must first find an opponent piece before our own
            while row_check in range(ROWS) and col_check in range(COLS):
                if self.board[row_check][col_check] == 0: # empty square so this direction is "no good"
                    break
                elif self.board[row_check][col_check].colour == opponent:
                    found_opponent =True
                    row_check += row_move
                    col_check +=col_move
                else: #we found our own piece
                    if found_opponent:
                        return True
                    else:
                        break
        return False # all directions ar "no good" -> illegal move.


    # had a bit of problem since im not using True vs False
    # so I cant use !self.turn , I keep using the opponent variable instead
    def get_opponent(self):
        return BLACK if self.turn == WHITE else WHITE

    def next_moves(self):
        next_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_legal(row, col):
                    next_moves.append((row,col))
        return next_moves

    # place the requested piece on the board and update the board
    def make_move(self, row, col):
        if not self.is_legal(row, col): #if this isn't a legal move do nothing.
          return
        self.board[row][col] = Piece(row,col,self.turn) # place the new piece
        self.turns_played += 1
        if self.turn == WHITE:
            self.white_pieces += 1
        else: #turn = black
            self.black_pieces += 1
        self.update_board(row,col)
        self.flip_turn()

    def update_board(self,row,col):
        opponent = self.get_opponent()
        # check in all directions which disks this move flips.
        for row_move, col_move in self.moves:
            pieces_to_flip = []
            row_check, col_check = row + row_move, col + col_move # check the square in move direction
            while row_check in range(ROWS) and col_check in range(COLS):
                piece = self.board[row_check][col_check]
                if piece == 0: # empty square "breaks" the line.
                    break
                elif piece.colour == opponent:
                    pieces_to_flip.append((row_check, col_check))
                    row_check += row_move
                    col_check += col_move
                elif piece.colour == self.turn: # this direction closes a line!
                    for flip_row, flip_col in pieces_to_flip:
                        self.board[flip_row][flip_col].colour = self.turn
                        if self.turn == BLACK:
                            self.black_pieces += 1
                            self.white_pieces -= 1
                        else:  # turn = White
                            self.white_pieces += 1
                            self.black_pieces -= 1
                    break
                else:  # shouldn't get here
                    break

    #flips turn
    def flip_turn(self):
        self.turn = BLACK if self.turn == WHITE else WHITE


# a bunch of different heuristics that I tried and pitted against each other.
# ultimately board_heuristic turned out to be the strongest.
    def heuristic_with_inside(self, turn):
        heuristic = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    continue
                sign = 1 if self.board[row][col].colour == turn else -1
                if is_corner(row, col):
                    heuristic += sign * CORNER_WEIGHT
                elif dangerous_square(row, col,self.board):
                    heuristic += sign * DANGEROUS_WEIGHT
                elif is_wall(row, col):
                    heuristic += sign * WALL_WEIGHT
                elif is_inside(row,col):
                    heuristic += sign * INSIDE_WEIGHT
                else:
                    heuristic += sign * 1
        return heuristic

    def heuristic_weak(self,turn):
        if turn == WHITE:
            return self.white_pieces - self.black_pieces
        else:
            return self.black_pieces - self.white_pieces



    # we are looking after turn is made
    # how many moves does oyr opponent have?
    # we want to  minimize it
    def mobility_heuristic(self):
        return  len(self.next_moves())


    def changing_heuristic(self, turn):
        if self.turns_played < TOTAL_PLYS * 0.7:
            return self.board_heuristic(turn)
        else:
            # focus on pieces in the end game
            return self.heuristic_weak(turn)

    def board_heuristic(self,turn):
        heuristic = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    continue
                sign = 1 if self.board[row][col].colour == turn else -1
                if is_corner(row,col):
                    heuristic += sign * CORNER_WEIGHT
                elif dangerous_square(row, col,self.board):
                    heuristic += sign * DANGEROUS_WEIGHT
                elif is_wall(row, col):
                    heuristic += sign * WALL_WEIGHT
                else:
                    heuristic += sign * 1
        normalized = (heuristic - MIN_SCORE)/ (MAX_SCORE-MIN_SCORE)
        return normalized


    def print_game_over(self):
        print("End state:")
        print(self)
        print(f"Result: white->{self.white_pieces} black-> {self.black_pieces}")
        if self.white_pieces > self.black_pieces:
            print("white wins!")
        elif self.black_pieces > self.white_pieces:
            print("black wins!")
        else:
            print("DRAW!!")