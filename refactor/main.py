from board import ReversiBoard
from reversi import AlphaBeta
BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'
BORDER = '#'

def main():

    board = ReversiBoard(8)
    board.showBoard()
    alphabeta = AlphaBeta(board)
    humanColor = input("please select your color, 'o' or 'x': ")
    assert humanColor in [BLACK, WHITE]
    board.setBothColor(humanColor)
    if humanColor == WHITE:
        comMove = board.genMove(board.computerColor)
        board.playMove(comMove,BLACK)
    while not board.isEnd():
        board.showBoard()
        print([board.point2position(point) for point in board.getLegalMoves(humanColor)])
        #move = input("Please enter the move: ")
        #valid, _ = board.isPositionValid(move, humanColor)
        #while not valid:
        #    move = input("Invalid move, please enter the move again: ")
        #    valid, _ = board.isPositionValid(move, humanColor)
        moves = board.getLegalMoves(humanColor)
        if not moves:
        	board.pass2 += 1
        	if board.pass2 == 2:
        		break
        	break
        else:
        	board.pass2 = 0
        move = board.genMove(humanColor)
        board.playMove(move,humanColor)
        board.showBoard()
        _, comMove = alphabeta.genMove(board.computerColor)
        if comMove:
        	board.pass2 = 0
        	print("computer make move", board.point2position(comMove))
        	board.playMove(comMove,board.computerColor)
        else:
        	board.pass2 += 1
        	if board.pass2 == 2:
        		break
        	break

    board.showBoard()
    winner = board.getWinner()
    blackScore = board.getScore(BLACK)
    whiteScore = board.getScore(WHITE)
    print(winner,"Wins")
    print("Black score", blackScore)
    print("White score", whiteScore)

main()