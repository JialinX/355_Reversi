from board import ReversiBoard
from greedy import greedy

def main():
    board = ReversiBoard(8)
    player1 = "b"
    player2 = "w"
    
    while True:
        board.showBoard()
        if board.isEnd():
            print("The winner is:",board.getWinner())
            break
        else:
            board.genMove(player1)
            point = greedy(board, player2)
            board.play(player2, point)
    
    
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