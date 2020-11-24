from board import ReversiBoard
from reversi import AlphaBetaGenMove
import random
import time

BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'

#######################
'''
TODO:
1. ADD welcome and guide message in the very beginning
2. change UI, remove board or '.'
3. board.showboard also shows both scores
4. if a move is generated by computer, show move position
5. !!!provide pass option if no legal moves
6. !!!Documentation
7. board.play doesnt work
8. update help menu with more intructions
9. undo() function doesnt actually undo board (see bugs in reversi ab steps)
'''
#######################

#class Cell:
    #chars ='bw' 
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def showLegalMove(board, player1):
    move = board.getAllLegalMoves(player1)
    print(move)
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

def getUserColor():
    print("x is black color stone, o is white color stone")
    while True:
        choose = input("Please specify the color of stone you want to use(x/o): ")
        if choose.lower() in ["o", "w", "white"]:
            return WHITE, BLACK
        elif choose.lower() in ["x", "b", "black"]:
            return BLACK, WHITE
        print("invalid input, please input again")
    
def showResult(board):
    winner = board.getWinner()
    if winner == "tie":
        "The game ties"
    else:
        print("The winner is:", winner, "with score of", board.getMark(winner))
    
def dealCommand(userInput, board, alphabeta):
    command = userInput.split()[0]
    if command =='h':
        board.printMenu()
    elif command =='x': #user play first
        position  = board.position2point(userInput.split()[1])
        #value, move = alphabeta.genMove(color)
        if position in board.getAllLegalMoves(BLACK):
            board.play(BLACK, position)
        else:
            print("invalid position for", BLACK)
        value, move = alphabeta.genMove(WHITE)
        board.play(WHITE, move)
    elif command =='o':#computer play first
        #print('here')
        position  = board.position2point(userInput.split()[1])
        #value, move = alphabeta.genMove(color)
        if position in board.getAllLegalMoves(WHITE):
            board.play(WHITE, move)
        else:
            print("invalid position for", WHITE)
        value, move = alphabeta.genMove(BLACK)
        board.play(BLACK, move)
    elif command =='.':
        pass
    elif command =='g':
        color = userInput.split()[1]
        value, move = alphabeta.genMove(color)
        print('recommand',value, move)
    elif command =='l':
        color = userInput.split()[1]
        showLegalMove(board, color)    
    elif command =='u':
        board.undo()
    elif command =='q':
        print('\n ... Bye :)\n')    
        return False
    
    
    board.showBoard()
    return True
    
def main():
    print("add message here")
    board = ReversiBoard(8)
    board.initBoard()
    alphabeta = AlphaBetaGenMove(board)

    score = {BLACK:2, WHITE:2}
    board.printMenu() 
    print()
    
    player1, player2 = getUserColor()
    board.showBoard()
    loop = True
    while loop:
        if board.isEnd():
            showResult(board)
            break 
        
        userInput = input("Command>> ")
        loop = dealCommand(userInput, board, alphabeta)
        


if __name__ == '__main__':
    main()
    
