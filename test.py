from board import ReversiBoard
def main():
    board = ReversiBoard(8)
    color = "b"
    while True:
        board.showBoard()
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
	    

if __name__ == '__main__':
    main()