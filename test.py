from board import ReversiBoard
from greedy import greedy
import random

def compete(board, player1, player2, gameNum, score):
    while True:
        board.showBoard()
        if board.isEnd():
            winner = board.getWinner()
            
            if winner == player1:
                score["Player1"] += 1
            elif winner == player2:
                score["Player2"] += 1
            break

        else:
            # player1 is random player
            moves = board.getAllLegalMoves(player1)
            board.play(player1, random.choice(moves))
            # import player2 here
            point = greedy(board, player2)
            board.play(player2, point) 


def main():
    board = ReversiBoard(8)
    player1 = "b"
    player2 = "w"
    gameNum = 10
    count = 0
    score = {"Player1": 0, "Player2": 0}
    while count != 10:
        compete(board, player1, player2, gameNum, score)
        count += 1
    print("Total game played:", gameNum)
    print(score)


if __name__ == '__main__':
    main()