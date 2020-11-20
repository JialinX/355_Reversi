from board import ReversiBoard
from greedy import greedy
import random

def main():
    board = ReversiBoard(8)
    player1 = "b"
    player2 = "w"
    gameNum = 10
    count = 1
    score = {"Player1": 0, "Player2": 0}
    while count != 11:
        while True:
            board.showBoard()
            if board.isEnd():
                winner = board.getWinner()
                
                if winner == player1:
                    score["Player1"] += 1
                elif winner == player2:
                    score["Player2"] += 1
                count += 1
                break
            else:
                # player1 is random player
                moves = board.getAllLegalMoves(player1)
                board.play(player1, random.choice(moves))
                point = greedy(board, player2)
                board.play(player2, point)
    print("Total game played:", gameNum)
    print(score)

    
    '''
        cmd = input('')
        if len(cmd)==0:
            print('\n ... adios :)\n')
            return
        if cmd[0][0]=='h':
            
            board.printMenu()
        elif cmd[0][0]=='p':
            
            board.genMove(color)
            if color == "b":
                color = "w"
            elif color == "w":
                color = "b"
        elif cmd =='b 19':
            board.erase(19)
            '''

if __name__ == '__main__':
    main()