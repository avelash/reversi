import pygame
from reversi.constants import SQUARE_SIZE, WHITE, PADDING

#class Piece represents a piece on that board.

class Piece:
    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 #for drawing
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 #for drawing

    def draw_piece(self,win):
        pygame.draw.circle(win, self.colour, (self.x, self.y), SQUARE_SIZE//2 - PADDING)

    def __repr__(self):
        return 'W' if self.colour == WHITE else 'B' #for printing board



