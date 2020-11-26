from board import ReversiBoard
from reversi import AlphaBeta
BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'
BORDER = '#'

def printResult(board):
    """
    printResult. Print the result of a given board state
    :return: none
    """
    print(f"The game winner is {board.getWinner()}")
    print(f"{BLACK} has score {board.getScore(BLACK)}")
    print(f"{WHITE} has score {board.getScore(WHITE)}")

def printMenu():
    """
    printMenu. Print the instruction menue 
    :return: none 
    """
    print('  h            help menu')
    print('  b            board')
    print('  x a2         play x at a2')
    print('  o g3         play o at g3')
    print('  g x/o        genmove for x/o')
    print('  l x/o        show legal moves for x/o')
    print('  p            pass your current turn')
    print('  u            undo')

def computerPlay(board, alphabeta, computerColor):
    """
    computerPlay. To check if there is any legal move for computer
    :param board: list. Indicate current board state
    :param alphabeta: class. Indicate alphabeta class
    :param computerColor: str. Indicate the computer's color
    """
    _, move = alphabeta.genMove(computerColor)
    if move is None:
        board.pass2 += 1
        print("computer has no legal move, then computer passes")
        if board.pass2 == 2:
            return False
        return True
    board.playMove(move, computerColor)
    board.pass2 = 0
    print("Computer's turn: ")
    board.showBoard()
    print(f"Computer played at {board.point2position(move)}")
    return True

def playCommand(board, point, alphabeta, color, humanColor, computerColor):
    """
    playCommand. To present the instructions to player
    :param board: list. Indicate current board state
    :param point: int. Indicate the index number of the given position
    :param alphabeta: class. Indicate alphabeta class
    :param color: str. Indicate the player's color
    :param humanColor: str. Indicate the player's color (pvp only)
    :param computerColor: str. Indicate the computer's color (pvp only)
    :return: if game ends
    """
    moves = board.getLegalMoves(color)
    if color == computerColor:
        print("You cannot play as computer's color")
        return True

    if not moves:
        board.pass2 += 1
        print(f"There is no legal moves for {color}, this turn has passed")
        if board.pass2 == 2:
            return False
        else:
            if humanColor == color:
                return computerPlay(board, alphabeta, computerColor)
            return True

    if point in moves:
        board.playMove(point, color)
        board.pass2 = 0
        board.showBoard()
    else:
        print(f"Invalid position for {color}, please select from following moves")
        showLegalMove(board, color)
        return True
    if humanColor == color:
        return computerPlay(board, alphabeta, computerColor)
        
        
    return True

def showLegalMove(board, color):
    """
    showLegalMove. To show legal moves for the current player
    :param board: list. Indicate current board state
    :param color: str. Indicate current player's color
    :return: boolean or str. Ture if no legal move found, otherwise a string of all legal moves
    """
    moves = board.getLegalMoves(color)
    if len(moves) == 0:
        print("You have no legal moves, enter 'p' to pass your turn")
        return False
    else:
        allMoves = " ".join([board.point2position(move) for move in moves])
        print(f"All legal moves for {color} are: {allMoves}")
        return True

def getHumanColor():
    """
    getHumanColor. To obtain player's color
    :return: str. Indicate player's chosen color
    """
    while True:
        print("Do you wanna play against computer? (y/n)")
        print("If y(es), computer will play with you")
        print("If n(o), the board is just for testing or pvp use")
        pve = input(">> ")
        if pve[0].lower() == 'y':
            print("x goes first, o goes second")
            color = input("What color do you want to use? (x/o): ")
            while color[0].lower() not in [BLACK,WHITE,'w','b']:
                color = input("Invalid, input, please input again: ")
            if color[0] in [BLACK,'b']:
                return BLACK
            else:
                return WHITE

        elif pve[0].lower() == 'n':
            return None
        
        else:
            print("Invalid input, please input again")


def dealCommand(commands, board, alphabeta, humanColor, computerColor):
    """
    dealCommand. To present the corresponding commend from the player
    :param commands: str. Indicate player's input
    :param board: list. Indicate current board state
    :param alphabeta: class. Indicate alphabeta class
    :param humanColor: str. Indicate the player's color
    :param computerColor: str. Indicate the computer's color
    :return: none
    """
    commandLen = len(commands.split())
    
    if commands[0] == 'h':
        printMenu()

    elif commands[0] == 'b':
        board.showBoard()

    elif commands[0] in [BLACK, WHITE]:
        if commandLen != 2:
            print("Invalid command, plese input again.")
            return True        
        
        _, position = commands.split()
        color = commands[0]
        point = board.position2point(position)
        return playCommand(board, point, alphabeta, color, humanColor, computerColor)

    elif commands[0] == 'g':
        if commandLen != 2:
            print("Invalid command, plese input again.")
            return True      
        
        _, color = commands.split()
        _, move = alphabeta.genMove(color)
        if move is not None:
            print(f"The best move found by AlphaBeta is {board.point2position(move)}")
        else:
            print("There are no move generated by Alphabeta")

    elif commands[0] == 'l':
        if commandLen != 2:
            print("Invalid command, plese input again.")
            return True        
        _, color = commands.split()
        showLegalMove(board, color)

    elif commands[0] == 'u':
        board.undo()
        board.showBoard()

    elif commands[0] == 'p':
        playCommand(board, 0, alphabeta, humanColor, humanColor, computerColor)

    elif commands[0] == 'q':
        print("Bye...:)")
        return False

    else:
        print("Invalid command, plese input again.") 

    return True

def main():

    board = ReversiBoard(8)
    board.showBoard()
    alphabeta = AlphaBeta(board)
    humanColor = getHumanColor()
    board.setBothColor(humanColor)
    computerColor = None if humanColor is None else board.computerColor

    if humanColor == WHITE:
        _, comMove = alphabeta.genMove(board.computerColor)
        board.playMove(comMove,BLACK)
        print(f"Computer played at {board.point2position(comMove)}")
        
    while not board.isEnd():
        board.showBoard()
        moves = board.getLegalMoves(BLACK) + board.getLegalMoves(WHITE)
        
        if len(moves) == 0:
            break
        if board.pass2 == 2:
            break
        command = input("Commands>> ")
        
        #try:
        toGo = dealCommand(command, board, alphabeta, humanColor,computerColor)
        #except:
            #print("Invalid command, plese input again.") 
            
        if not toGo:
            break
    printResult(board)
    
main()
