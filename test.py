from board import ReversiBoard
from greedy import greedy
import math
import random
import time
def compete(board, player1, player2, gameNum, score):
    while True:
        #board.showBoard()
        if board.isEnd():
            winner = board.getWinner()
            if winner == player1:
                score["Player1"] += 1
            elif winner == player2:
                score["Player2"] += 1
            else:
                score["Tie"] += 1
            break

        else:
            # player1 is random player
            #time.sleep(5)
            moves = board.getAllLegalMoves(player1)
            if len(moves) != 0:
                board.play(player1, random.choice(moves))
            # import player2 here
            #board.showBoard()
            #time.sleep(5)
            #moves = board.getAllLegalMoves(player2)
            #board.play(player2, random.choice(moves))
            moves = board.getAllLegalMoves(player2)
            if len(moves) != 0:
                point = greedy(board, player2)
                board.play(player2, point) 


def main():
    player1 = "b"
    player2 = "w"
    gameNum = 10000
    count = 0
    score = {"Player1": 0, "Player2": 0, "Tie": 0}
    while count != gameNum:
        board = ReversiBoard(8)
        compete(board, player1, player2, gameNum, score)
        count += 1
        if count == 10 or count == 100 or count == 1000 or count == 10000:
            winRate = {"player1": round(score["Player1"]/count*100,1),"player2":round(score["Player2"]/count*100, 1)}
            print("+----------+----------+---------------")
            print("Total game played:", count)
            print("+----------+----------+---------------")
            print("| Players  | Win rate |") 
            print("+----------+----------+---------------")
            print("|", "Player1"," |",str(winRate["player1"]),"%","  |")
            print("+----------+----------+---------------")
            print("|", "Player2"," |",str(winRate["player2"]),"%","  |")
            print("+----------+----------+---------------")
            print("|","Tie      |", round(score["Tie"]/count*100,1),"%","   |")
            print("+----------+----------+---------------")
            



if __name__ == '__main__':
    main()