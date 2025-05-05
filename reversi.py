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
    board.print_game_over()


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



def min_max_game(num):
    board = Board()
    opponent_stuck = False
    while True:
        next_moves = board.next_moves()
        if len(next_moves) == 0:
            if opponent_stuck:
                break  # both players are stuck
            else:
                opponent_stuck = True
                board.flip_turn()
                continue
        best_move = min_max_search(board,board.turn,num)
        row, col = best_move
        board.make_move(row, col)
        opponent_stuck = False  # board has been changed
    board.print_game_over()


def min_max_search(board,player,num):
    # get the biggest possible score after num moves
    # only interested in the move not the score
    move, _ = max_score(board,player,num)
    return move


def max_score(board, player, num):
    next_moves = board.next_moves()
    num -= 1 # we are one depth deeper
    if len(next_moves) == 0: #no moves ahead
        return None, board.board_heuristic(player)# we will fix

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





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--displayAllActions", type=int,
                        help= "display all actions from a position with num disks")
    parser.add_argument("--methodical", type=int,
                        help="run a methodical game displaying the first n states")
    parser.add_argument("H",help= "run a game using heuristic for next move" )
    parser.add_argument("--ahead", type= int, default= 1, help="specify how many moves to look ahead, default 1")
    args = parser.parse_args()
    if args.displayAllActions:
        display_all_actions(args.displayAllActions)
    if args.methodical:
        methodical(args.methodical)
    if args.H:
        min_max_game(args.ahead)



if __name__ == '__main__':
    main()
