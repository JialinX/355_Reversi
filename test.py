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
            print(color)
            board.genMove(color)
            if color == "b":
                color = "w"
            elif color == "w":
                color = "b"
	    

if __name__ == '__main__':
    main()