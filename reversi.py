from reversi.board import Board
from reversi.constants import WHITE
import argparse


def methodical(n):
    board = Board()
    opponent_stuck = False
    while True:
        next_moves = board.next_moves()
        if len(next_moves) > 0:
            row, col = next_moves[0]
            board.make_move(row, col)
            opponent_stuck = False  # new move has been made
            if board.turns_played <= n:
                print(board)
        else:  # no moves for this player
            if opponent_stuck:
                break  # both players stuck -> game over
            else:
                opponent_stuck = True
                board.flip_turn()  # maybe other player has moves
    print("End state:")
    print(board)
    print(f"Result: player 1: {board.white_pieces} disks, player 2: {board.black_pieces} disks")
    if board.white_pieces == board.black_pieces:
        print("DRAW!!")
        return
    winner = "player 1" if board.white_pieces > board.black_pieces else "player 2"
    print(f"{winner} wins!")


def display_all_actions(num):
    # create board with num pieces
    board = Board()
    num -= board.white_pieces + board.black_pieces  # we already have some pieces on the board
    for i in range(num):
        next_moves = board.next_moves()
        next_move = next_moves[0]
        row, col = next_move
        board.make_move(row, col)

    print(f"Player 1 - W, Player 2 - B\n")
    to_play = "player 1" if board.turn == WHITE else "player 2"
    print(board)
    # display all Actions from current state
    next_moves = board.next_moves()
    for move in next_moves:
        row, col = move
        temp_board = board.copy()
        temp_board.make_move(row, col)
        print(f"{to_play} moved, Action: {move}")
        print(temp_board)
        print(f"Result: player 1: {temp_board.white_pieces} disks, player 2: {temp_board.black_pieces} disks,"
              f"total disks: {temp_board.black_pieces + temp_board.white_pieces}")
        print()  # empty row for clean prints


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--displayAllActions", type=int,
                        help= "display all actions from a position with num disks")
    parser.add_argument("--methodical", type=int,
                        help="run a methodical game displaying the first n states")
    args = parser.parse_args()
    if args.displayAllActions:
        display_all_actions(args.displayAllActions)
    if args.methodical:
        methodical(args.methodical)



if __name__ == '__main__':
    main()
