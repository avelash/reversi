from time import sleep
import pygame
from reversi.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE, MAX_SCORE
from reversi.board import Board
from reversi.helpers import min_max_search

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
    opponent_stuck = False


    while run:
        next_moves = board.next_moves()
        if len(next_moves) == 0:
            if opponent_stuck:
                break
            else:
                opponent_stuck = True
                board.flip_turn()
                continue
        if board.turn == WHITE:
            best_move = min_max_search(board,board.turn,3)
            row, col = best_move
            sleep(1)
            board.make_move(row, col)




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
    print(f"Result: white->{board.white_pieces} black-> {board.black_pieces}")
    if board.white_pieces > board.black_pieces:
        print("white wins!")
    elif board.black_pieces > board.white_pieces:
        print("black wins!")
    else:
        print("DRAW!!")
    pygame.quit()

if __name__ == '__main__':
    main()