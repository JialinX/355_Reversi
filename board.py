import numpy as np
from copy import deepcopy
BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'


class ReversiBoard():

    def __init__(self, size):
        """
        __init__. To initialize class variables
        :param size: int。 size of the board
        """
        self.size = size
        self.board = [EMPTY]*(self.size*self.size)
        self.boardHistory = []
        self.currentPlayer = BLACK
        self.directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.changedPoints = {}
        self.history = {}  
        self.boardHistory.append([
                '.', '.', '.', '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.', '.', '.', '.',
                '.', '.', '.', 'o', 'x', '.', '.', '.',
                '.', '.', '.', 'x', 'o', '.', '.', '.',
                '.', '.', '.', '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.', '.', '.', '.'])    

    def initBoard(self):
        """
        initBoard. To initialize the start position of the game board
        """
        mid = int(self.size/2)
        self.board[self.index2point(mid,mid)] = WHITE
        self.board[self.index2point(mid-1,mid-1)] = WHITE
        self.board[self.index2point(mid,mid-1)] = BLACK
        self.board[self.index2point(mid-1,mid)] = BLACK

    def showBoard(self):
        """
        showBoard. To construct the structure of the board
        :print: the constructed game board
        """
        colString = " " + "".join([str(i).center(3) for i  in range(1,self.size+1)])
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        board2d = self.boardTo2d()
        #sep  = f"  +{'-' * (3*self.size + self.size-1)}+"
        print(colString)
        #print(sep)
        for row in range(self.size):
            strRow = [str(i).center(3) for i in board2d[row]]
            #rowString =  str(alphabet[row]) + " |" + "|".join(strRow) + "|"
            rowString =  str(alphabet[row]) + "".join(strRow)
            print(rowString)
            #print(sep)
        
    def boardTo2d(self):
        """
        boardTo2d. Convert the constructed 3D board into 2D array
        :return: a list contain the board information
        """
        board2d = [[0 for i in range(self.size)] for j in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                point = self.index2point(row,col)
                board2d[row][col] = self.board[point]
        return board2d

    def printMenu(self):
        """
        printMenu. To print the information menu for the player

        """
        print('  h            help menu')
        print('  b            board')
        print('  x a2         play x at a2')
        print('  o g3         play o at g3')
        print('  . e3         erase e3')
        print('  g x/o        genmove for x/o')
        print('  l x/o        show legal moves for x/o')
        print('  u            undo')

    def board2string(self, state):
        """
        board2string. To convert board data to type str
        :param state: array of lists. Indicate the current board state
        :return: str board
        """

        boardString = ""
        for ix,iy in np.ndindex(state.shape):
            boardString += state[ix,iy]

        return boardString

    def getIso(self):
        """
        getIso. To obtain all the isomorphic board states of a specific board state
        :return: list. Containing all the isomorphic strings of a given board state
        """

        npboard = np.array(self.board)
        board2d = np.reshape(npboard, (-1, 2))
        leftRightFlipBoard = np.fliplr(board2d)
        upDownFlipBoard = np.flipud(board2d)
        isoString = [self.board2string(board2d),self.board2string(np.rot90(board2d, 1)),
                    self.board2string(np.rot90(board2d, 2)),self.board2string(np.rot90(board2d, 3)),
                    self.board2string(upDownFlipBoard),self.board2string(leftRightFlipBoard),
                    self.board2string(np.rot90(leftRightFlipBoard,1)),self.board2string(np.rot90(upDownFlipBoard,1))]

        return isoString

    def addHistory(self, score):
        """
        addHistory. To add Key/Value combination into history dictionary
        :param score:int. Indicate the score received for a given board state
        """
        state = ''.join(self.board)
        self.history[state] = score

    def getHistory(self):
        """
        getHistory. To obtain the historical game states
        :return: return the game history otherwise return False
        """

        boardIso = self.getIso()
        for state in boardIso:
            if state in self.history:
                return self.history[state]
        return False

   
    def position2point(self, position):
        """
        position2point. To obtain an index value for a position given its position code
        :param position: list. Indicate a position code containing letter and column number
        :return: int. Return an index of this position given its row and col numbers
        """
        letter, col = position
        col = int(col)
        col -= 1
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        row = alphabet.index(letter)

        return self.index2point(row,col)

    def index2point(self, row, col):
        """
        index2point. To obtain an index value for a position given its row and col numbers
        :param row: int. Indicate row position
        :param col: int. Indicate col position
        :return: int. Return an index of this position given its row and col numbers
        """

        return (self.size) * row + col

    def point2position(self,point):
        """
        point2position. To convert an index for a position to its row and col representation
        :param point: int. Indicating this index number of the given position
        :return: list. Containing the given index's row and col number
        """

        return point// self.size,point % self.size
    
    def point2LetterPosition(self,point):
        """
        point2LetterPosition. To convert an index for a position to its position code
        containing letter and column number
        :param point: int. Indicating the index number of the given position
        :return: str. Containing letter and column number to represent the given position
        """
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        return alphabet[point//self.size]+str(point % self.size+1)  
    
    def getAllLegalMoves(self, color):
        """
        getAllLegalMoves. To obtain all the legal moves of color's current position
        :param color: str. Indicate current player's color
        :return: a list containing legal moves of current position
        """
        legalMove = []
        for point in range(len(self.board)):
            if self.board[point] == EMPTY:
                position = self.point2position(point)
                if self.reverseColor(position, color, "check"):
                    legalMove.append(point)
        return legalMove


    def erase(self, point):
        """
        erase. To delete a move from the game board
        :param point: int. Indicating the index number of the given position
        :return: none
        """
        self.board[point] = EMPTY
        for key in self.changedPoints:
            self.board[key] = self.changedPoints[key]
        self.changedPoints = {}

    def play(self, color, point):
        """
        play. To make a move on the game board
        :param color: str. Indicate current player's color
        :param point: int. Indicating the index number of the given position
        :return: none
        """
        if self.board[point] == EMPTY:
            self.board[point] = color
        position = self.point2position(point)
        self.reverseColor(position, color,"change")
        self.boardHistory.append(deepcopy(self.board))
        
    def undo(self):
        """
        undo. To delete a board history from the list
        :return: none
        """
        self.boardHistory.pop()
        self.board = deepcopy(self.boardHistory[-1])
        
    def valid_move(self,i,j,i_step,j_step,color):
        """
        valid_move. To check if a position is a valid move
        :param i: int. Indicate row position
        :param j: int. Indicate col position
        :param i_step: int. Indicate row directional instruction
        :param j_step: int. Indicate col directional instruction
        :param color: str. Indicate current player's color
        :return: boolean.
        """
        #check if the adjacent cells has the same color
        #if it's the same color or empty, stop
        point = self.index2point(i,j)
        if self.board[point] == color or self.board[point] == EMPTY or point < 0:
            return False

        return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)


    def check_directions(self,i,j,i_step,j_step,color):
        """
        check_directions.
        :param i: int. Indicate row position
        :param j: int. Indicate col position
        :param i_step: int. Indicate row directional instruction
        :param j_step: int. Indicate col directional instruction
        :param color: str. Indicate current player's color
        :return: boolean.
        """
        point = self.index2point(i,j)
        if self.board[point] == color:
            return True

        elif self.board[point] == EMPTY or point < 0:
            return False

        else:
            return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)


    def reverseColor(self,position,color,code):
        """
        reverseColor. To reverse a player's color to its opponent's color
        :param position: list. Indicate the row and col position
        :param color: str. Indicate current player's color
        :param code: str. Indicate the instruction
        :return: none
        """
        #check moves
        i,j = position
        for dire in self.directions:
            i_step,j_step = dire
            try:
                if i+i_step >= 0 and i+i_step < self.size and j+j_step >=0 and j+j_step < self.size:
                    valid = self.valid_move(i+i_step,j+j_step,i_step,j_step,color)
                    if valid and code == "check":
                        return True
                    elif valid and code == "change":
                        self.start_reverse(i+i_step,j+j_step,i_step,j_step,color)
            except:
                pass


    def start_reverse(self,i,j,i_step,j_step,color):
        """
        start_reverse. To reverse the opponent's color for a given move
        :param i: int. Indicate row position
        :param j: int. Indicate col position
        :param i_step: int. Indicate row directional instruction
        :param j_step: int. Indicate col directional instruction
        :param color: str. Indicate current player's color
        :return: none
        """
        if color == WHITE:
            optcolor = BLACK
        else:
            optcolor = WHITE
        point = self.index2point(i,j)
        if self.board[point] == color:
            return
        self.board[point] = color
        self.changedPoints[point] = optcolor
        self.start_reverse(i+i_step, j+j_step, i_step, j_step, color)


    def getMark(self, color):
        """
        getMark. To obtain the marks for the given player
        :param color: str. Indicate player's color
        :return: int. Indicate given player's marks
        """
        mark = 0
        for point in self.board:
            if point == color:
                mark += 1
        return mark

    def isEnd(self):
        """
        isEnd. To check if the game is end
        :return: boolean. Return True if the game is end, otherwise return False
        """
        if len(self.getAllLegalMoves(BLACK)) == 0 and len(self.getAllLegalMoves(WHITE)) == 0:
            return True
        else:
            return False


    def getWinner(self):
        """
        getWinner. To compare player's marks and get the one with higher marks
        :return: str. Indicate the winner or draw condition
        """
        if self.isEnd():
            blackMark = self.getMark(BLACK)
            whiteMark = self.getMark(WHITE)
            if blackMark > whiteMark:
                return BLACK
            elif blackMark == whiteMark:
                return 'tie'
            else:
                return WHITE

        return None

    def change_current_player(self):
        """
        change_current_player. To switch the state of current player
        :return: none
        """

        self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE
    
    def getOptColor(self, color):
        """
        getOptColor. To obtain the opponent player's color
        :param color: str. Indicate current player's color
        :return: str. Indicate the opponent player's color
        """
        if color == BLACK:
            return WHITE
        if color == WHITE:
            return BLACK
         
