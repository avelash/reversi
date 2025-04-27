import pygame
import time
from reversi.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, BLACK
from reversi.board import Board
from reversi.piece import Piece
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Reversi_AI')


def get_row_and_col_from_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()




    while run:
        # if board.turn == BLACK:
        #     next_moves = board.next_moves()
        #     if len(next_moves) == 0:
        #         break
        #     next_move = next_moves[0]
        #     row, col = next_move
        #     time.sleep(3)
        #     board.make_move(row, col)

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_and_col_from_pos(pos)
                if board.is_legal(row,col):
                    board.make_move(row,col)




        board.draw_board(WIN)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()