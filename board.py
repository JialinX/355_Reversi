import numpy as np
from copy import deepcopy
BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'


class ReversiBoard():

    def __init__(self, size):
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
        mid = int(self.size/2)
        self.board[self.index2point(mid,mid)] = WHITE
        self.board[self.index2point(mid-1,mid-1)] = WHITE
        self.board[self.index2point(mid,mid-1)] = BLACK
        self.board[self.index2point(mid-1,mid)] = BLACK

    def showBoard(self):
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
        board2d = [[0 for i in range(self.size)] for j in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                point = self.index2point(row,col)
                board2d[row][col] = self.board[point]
        return board2d

    def printMenu(self):
        print('  h            help menu')
        print('  b            board')
        print('  x a2         play x at a2')
        print('  o g3         play o at g3')
        print('  . e3         erase e3')
        print('  g x/o        genmove for x/o')
        print('  l x/o        show legal moves for x/o')
        print('  u            undo')

    def board2string(self, state):

        boardString = ""
        for ix,iy in np.ndindex(state.shape):
            boardString += state[ix,iy]

        return boardString

    def getIso(self):

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
        state = ''.join(self.board)
        self.history[state] = score

    def getHistory(self):

        boardIso = self.getIso()
        for state in boardIso:
            if state in self.history:
                return self.history[state]
        return False

   
    def position2point(self, position):
        letter, col = position
        col = int(col)
        col -= 1
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        row = alphabet.index(letter)

        return self.index2point(row,col)

    def index2point(self, row, col):

        return (self.size) * row + col

    def point2position(self,point):

        return point// self.size,point % self.size
    
    def point2LetterPosition(self,point):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        return alphabet[point//self.size]+str(point % self.size+1)  
    
    def getAllLegalMoves(self, color):
        legalMove = []
        for point in range(len(self.board)):
            if self.board[point] == EMPTY:
                position = self.point2position(point)
                if self.reverseColor(position, color, "check"):
                    legalMove.append(point)
        return legalMove


    def erase(self, point):
        self.board[point] = EMPTY
        for key in self.changedPoints:
            self.board[key] = self.changedPoints[key]
        self.changedPoints = {}

    def play(self, color, point):
        if self.board[point] == EMPTY:
            self.board[point] = color
        position = self.point2position(point)
        self.reverseColor(position, color,"change")
        self.boardHistory.append(deepcopy(self.board))
        
    def undo(self):
        self.boardHistory.pop()
        self.board = deepcopy(self.boardHistory[-1])
        
    def valid_move(self,i,j,i_step,j_step,color):
        #check if the adjacent cells has the same color
        #if it's the same color or empty, stop
        point = self.index2point(i,j)
        if self.board[point] == color or self.board[point] == EMPTY or point < 0:
            return False

        return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)


    def check_directions(self,i,j,i_step,j_step,color):
        point = self.index2point(i,j)
        if self.board[point] == color:
            return True

        elif self.board[point] == EMPTY or point < 0:
            return False

        else:
            return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)


    def reverseColor(self,position,color,code):
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
        mark = 0
        for point in self.board:
            if point == color:
                mark += 1
        return mark

    def isEnd(self):
        if len(self.getAllLegalMoves(BLACK)) == 0 and len(self.getAllLegalMoves(WHITE)) == 0:
            return True
        else:
            return False


    def getWinner(self):
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

        self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE
    
    def getOptColor(self, color):
        if color == BLACK:
            return WHITE
        if color == WHITE:
            return BLACK
         
