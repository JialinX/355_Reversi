import numpy as np
from copy import deepcopy
from tkinter import *
from time import *
from reversi import AlphaBetaGenMove

BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'

#Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222",highlightthickness=0)
screen.pack()

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
        self.oldboard = [EMPTY]*(self.size*self.size)
        self.newboard = [EMPTY]*(self.size*self.size)

    def update(self):
        print('update')
        screen.delete("highlight")
        screen.delete("tile")
        board2d = self.boardTo2d(self.board)
        oldboard2d = self.boardTo2d(self.oldboard)
        print(board2d)
        print(oldboard2d)
        for x in range(8):
            for y in range(8):
                #Could replace the circles with images later, if I want
                if oldboard2d[x][y]=="o":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

                elif oldboard2d[x][y]=="x":
                    screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                    screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
        #Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
                #Could replace the circles with images later, if I want
                if board2d[x][y]!=oldboard2d[x][y] and board2d[x][y]=="o":
                    screen.delete("{0}-{1}".format(y,x))
                    #42 is width of tile so 21 is half of that
                    #Shrinking
                    for i in range(21):
                        screen.create_oval(54+i+50*y,54+i+50*x,96-i+50*y,96-i+50*x,tags="tile animated",fill="#000",outline="#000") #black
                        screen.create_oval(54+i+50*y,52+i+50*x,96-i+50*y,94-i+50*x,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    #Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*y,54+i+50*x,96-i+50*y,96-i+50*x,tags="tile animated",fill="#aaa",outline="#aaa") #grey
                        screen.create_oval(54+i+50*y,52+i+50*x,96-i+50*y,94-i+50*x,tags="tile animated",fill="#fff",outline="#fff") #white
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54+50*y,54+50*x,96+50*y,96+50*x,tags="tile",fill="#aaa",outline="#aaa")
                    screen.create_oval(54+50*y,52+50*x,96+50*y,94+50*x,tags="tile",fill="#fff",outline="#fff")
                    screen.update()

                elif board2d[x][y]!=oldboard2d[x][y] and board2d[x][y]=="x":
                    screen.delete("{0}-{1}".format(y,x))
                    #42 is width of tile so 21 is half of that
                    #Shrinking
                    for i in range(21):
                        screen.create_oval(54+i+50*y,54+i+50*x,96-i+50*y,96-i+50*x,tags="tile animated",fill="#aaa",outline="#aaa")
                        screen.create_oval(54+i+50*y,52+i+50*x,96-i+50*y,94-i+50*x,tags="tile animated",fill="#fff",outline="#fff")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    #Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54+i+50*y,54+i+50*x,96-i+50*y,96-i+50*x,tags="tile animated",fill="#000",outline="#000")
                        screen.create_oval(54+i+50*y,52+i+50*x,96-i+50*y,94-i+50*x,tags="tile animated",fill="#111",outline="#111")
                        if i%3==0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54+50*y,54+50*x,96+50*y,96+50*x,tags="tile",fill="#000",outline="#000")
                    screen.create_oval(54+50*y,52+50*x,96+50*y,94+50*x,tags="tile",fill="#111",outline="#111")
                    screen.update()
        
        moves = self.getAllLegalMoves(BLACK)
        for m in moves:
            x=int(self.point2position(m)[0])
            y=int(self.point2position(m)[1])
            screen.create_oval(68+50*y,68+50*x,32+50*(y+1),32+50*(x+1),tags="highlight",fill="#008000",outline="#008000")
        
        if not self.isEnd():
            #Draw the scoreboard and update the screen
            self.drawScoreBoard()
            screen.update()
            #If the computer is AI, make a move
            print(self.currentPlayer)
            if self.currentPlayer==WHITE:
                value, move = alphabeta.genMove(WHITE)
                print(value,move)
                self.makeMove(move)
        else:
            screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")

    def drawScoreBoard(self):
        global moves
        #Deleting prior score elements
        screen.delete("score")
        board2d = self.boardTo2d(self.board)
        #Scoring based on number of tiles
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if board2d[x][y]=="x":
                    player_score+=1
                elif board2d[x][y]=="o":
                    computer_score+=1

        if self.currentPlayer==BLACK:
            player_colour = "green"
            computer_colour = "gray"
        else:
            player_colour = "gray"
            computer_colour = "green"

        screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
        screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

        #Pushing text to screen
        screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
        screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

        moves = player_score+computer_score

    def initBoard(self):
        mid = int(self.size/2)
        self.board[self.index2point(mid,mid)] = WHITE
        self.board[self.index2point(mid-1,mid-1)] = WHITE
        self.board[self.index2point(mid,mid-1)] = BLACK
        self.board[self.index2point(mid-1,mid)] = BLACK
        self.oldboard = deepcopy(self.board)
        self.newboard = deepcopy(self.board)

    def showBoard(self):
        colString = "   " + " ".join([str(i).center(3) for i  in range(1,self.size+1)])
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        board2d = self.boardTo2d(self.board)
        sep  = f"  +{'-' * (3*self.size + self.size-1)}+"
        print(colString)
        print(sep)
        for row in range(self.size):
            strRow = [str(i).center(3) for i in board2d[row]]
            rowString =  str(alphabet[row]) + " |" + "|".join(strRow) + "|"
            print(rowString)
            print(sep)
        
    def boardTo2d(self,board):
        board2d = [[0 for i in range(self.size)] for j in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                point = self.index2point(row,col)
                board2d[row][col] = board[point]
        return board2d

    def printMenu(self):
        print('  h            help menu')
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
    
    def getAllLegalMoves(self, color):
        legalMove = []
        for point in range(len(self.board)):
            if self.board[point] == EMPTY: # to be changed to all adjcent cells instead of empty cells
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
        # self.showBoard()
        self.boardHistory.append(deepcopy(self.board))

    def makeMove(self, color, point):
        print(color,point)
        self.oldboard = deepcopy(self.board)
        if self.board[point] == EMPTY:
            self.board[point] = color
        self.newboard = deepcopy(self.board)
        position = self.point2position(point)
        self.reverseColor(position, color,"change")
        self.change_current_player()
        self.showBoard()
        self.update()
        self.boardHistory.append(deepcopy(self.board))
        
    def undo(self):
        self.oldboard = deepcopy(self.board)
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

def finalHeuristic(self, color):
    total = 0
    board2d = self.board.boardTo2d(self.board)
    self.board.showBoard()
    
    for i in range(self.board.size):
        for j in range(self.board.size):
            if board2d[i][j] == color:
                total += self.weight[i][j]
    return total

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
    global depth
    xMouse = event.x
    yMouse = event.y

    if running:
        print(board.currentPlayer)
        board2d = board.boardTo2d(board.board)
        if xMouse>=450 and yMouse<=50:
            root.destroy()
        elif xMouse<=50 and yMouse<=50:
            playGame()   
        else:
            #Is it the player's turn?
            if board.currentPlayer==BLACK:
                #Delete the highlights
                x = int((event.x-50)/50)
                y = int((event.y-50)/50)
                moves = board.getAllLegalMoves(BLACK)
               
                for m in moves:
                    row=int(board.point2position(m)[0])
                    col=int(board.point2position(m)[1])
                    print(y,row,'|||',x,col)
                    if(y==row and col == x):
                        print(m)
                        board.makeMove(BLACK,m)
    else:
    	playGame()

def keyHandle(event):
    symbol = event.keysym
    if symbol.lower()=="r":
        playGame()
    elif symbol.lower()=="q":
        root.destroy()

def create_buttons():
        #Restart button
        #Background/shadow
        screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
        screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

        #Arrow
        screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
        screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

        #Quit button
        #Background/shadow
        screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
        screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
        #"X"
        screen.create_line(455,5,495,45,fill="white",width="3")
        screen.create_line(495,5,455,45,fill="white",width="3")
    
def runGame():
    global running
    running = False
    #Title and shadow
    screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
    screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
    
    #Creating the difficulty buttons
    for i in range(3):
        #Background
        screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
        screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")

        spacing = 130/(i+2)
        for x in range(i+1):
            #Star with double shadow
            screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
            screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
            screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")
    screen.update()

def drawGridBackground(outline=False):
	#If we want an outline on the board then draw one
	if outline:
		screen.create_rectangle(50,50,450,450,outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical line
		screen.create_line(lineShift,50,lineShift,450,fill="#111")

	screen.update()


def playGame():
    global board, running, alphabeta
    running = True
    screen.delete(ALL)
    create_buttons()
    board = 0
    #Draw the background
    drawGridBackground()
    #Create the board and update it
    board = ReversiBoard(8)
    alphabeta = AlphaBetaGenMove(board)
    board.initBoard()
    board.update()         

runGame()

screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("Othello")
root.mainloop()