from board import ReversiBoard
import random
import time
class Cell:
  chars ='bw' 
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def showLegalMove(board, player1):
    move = board.getAllLegalMoves(player1)
    if len(move) == 0:
        print("You have no legal move!")
        return True
    else:
        print("Here are all the legal moves:")
        coord = []
        for i in move:
            position = board.point2position(i)
            letter = alphabet[position[0]]
            coord.append(letter+str(position[1]+1))      
        print(coord) 


def main():
    board = ReversiBoard(8)
    score = {"player1":0,"player2":0}
    while True:
        choose = input("Please specify the color of stone you want to use: ")
        if choose.lower() == "w" or choose.lower() == "white":
            player1 = "w"
            player2 = "b"
            break
        elif choose.lower() == "b" or choose.lower() == "black":
            player1 = "b"
            player2 = "w"
            break

    board.printMenu() 
    while True:
        if board.isEnd():
            winner = board.getWinner() 
            if winner == player1:
                print("The winner is:", winner)
                score["Player1"] = board.getMark(player1)
            elif winner == player2:
                print("The winner is:", winner)
                score["Player2"] = board.getMark(player2)
            else:
                print("tie")
            return 
        else:
            board.showBoard()
            #show legal moves
            showLegalMove(board, player1)

            #get user input
            cmd = input('')
            if len(cmd)==0:         
                print('\n ... adios :)\n')              
                return              
            if cmd[0][0]=='h':                        
                board.printMenu()               
            elif cmd[0][0] in Cell.chars:                                 
                check = board.makeMove(cmd)  
                # if the player make a valid move, player2 will play automatically  
                if check: 
                    moves = board.getAllLegalMoves(player2)
                    board.play(player2, random.choice(moves))
                    #point = greedy(board, player2)
                   # board.play(player2, point)          


if __name__ == '__main__':
    main()