import pygame
import time
from reversi.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from reversi.board import Board

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
        best_move = next_moves[0]
        row, col = best_move
        if board.turn == WHITE:
            best_move_h = board.heuristic2(row, col)
            for move in next_moves:
                row, col = move
                if board.heuristic2(row, col) > best_move_h:
                    best_move = move
                    best_move_h = board.heuristic2(row, col)
        else:
            best_move_h = board.heuristic(row, col)
            for move in next_moves:
                row, col = move
                if board.heuristic(row, col) > best_move_h:
                    best_move = move
                    best_move_h = board.heuristic(row, col)
        row, col = best_move
        time.sleep(1)
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