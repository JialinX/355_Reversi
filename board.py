BLACK = 'b' # player black
WHITE = 'w' # player white
EMPTY = '.'

class ReversiBoard():

    def __init__(self, size):
        self.size = size
        self.board = [EMPTY]*(self.size*self.size)
        self.initBoard()
        self.currentPlayer = BLACK
        self.directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    def initBoard(self):
        mid = int(self.size/2)
        self.board[self.index2point(mid,mid)] = WHITE
        self.board[self.index2point(mid-1,mid-1)] = WHITE
        self.board[self.index2point(mid,mid-1)] = BLACK
        self.board[self.index2point(mid-1,mid)] = BLACK

    def showBoard(self):
        colString = "   " + " ".join([str(i).center(3) for i  in range(1,self.size+1)])
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        board2d = self.boardTo2d()
        sep  = f"  +{'-' * (3*self.size + self.size-1)}+"
        print(colString)
        print(sep)
        for row in range(self.size):
            strRow = [str(i).center(3) for i in board2d[row]]
            rowString =  str(alphabet[row]) + " |" + "|".join(strRow) + "|"
            print(rowString)
            print(sep)
        
    def boardTo2d(self):
        board2d = [[0 for i in range(self.size)] for j in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                board2d[row][col] = self.board[(self.size) * row + col]
        return board2d

    def printMenu(self):
        print('  h            help menu')
        print('  x a2         play x a 2')
        print('  o g3         play o g 3')
        print('  . e3         erase e 3')
        print('  g x/o        genmove for x/o')
        print('  l x/o        show legal moves for x/o')
        print('  u            undo')

    def genMove(self, color):
        moves = self.getAllLegalMoves(color)
        pass

    #convert position str like "a1" to point like 0 as the index in self.board
    def position2point(self, position):
        letter, col = position
        col -= 1
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        row = alphabet.index(letter)

        return self.index2point(row,col)

    def index2point(self, row, col):

        return (self.size) * row + col

    def point2position(self,point):

        return point// self.size,point % self.size
    
    def getAllLegalMoves(self, color):
        markBefore = self.getMark(optColor)
        legalMoves = []
        for point in self.board:
            if point == EMPTY: # to be changed to all adjcent cells instead of empty cells
                
                self.play(color, point)
                if self.getMark(color) != markBefore:
                    legalMoves.append(point)
                self.erase(point)

        return legalMoves

    def erase(self,  point):
        self.board[point] = EMPTY

    def play(self, color, point):
        if self.board[point] == EMPTY:
            self.board[point] = color
        position = self.point2position(point)
        self.reverseColor(position, color)
        self.change_current_player()

    def valid_move(self,i,j,i_step,j_step,color):

        point = self.index2point(i,j)
        if self.board[point] == color or self.board[point] == EMPTY:
            return False,None

        return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)


    def check_directions(self,i,j,i_step,j_step,color):

        point = self.index2point(i,j)
        if self.board[point] == color:
            return True,[i,j]

        elif self.board[point] == EMPTY:
            return False,None

        else:
            return self.check_directions(i+i_step, j+j_step, i_step, j_step, color)

    def reverseColor(self,position,color):

        i,j = position
        for dire in self.directions:
            i_step,j_step = dire
            try:
                valid,end = self.valid_move(i+i_step,j+j_step,i_step,j_step,color)
                if valid and end:
                    self.start_reverse(i+i_step,j+j_step,i_step,j_step,color)
            except:
                pass


    def start_reverse(self,i,j,i_step,j_step,color):

        point = self.index2point(i,j)
        if self.board[point] == color:
            return
        self.board[point] = color

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


    