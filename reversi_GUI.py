import numpy as np
from copy import deepcopy
from time import *
from reversi import AlphaBeta
import random
from board import ReversiBoard
from tkinter import *

BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.' # empty point
BORDER = '#' # border point


root = Tk()
screen = Canvas(root, width=500, height=600, background="#e0e0e0",highlightthickness=0)
screen.pack()

def keyHandle(event):
    symbol = event.keysym
    if symbol.lower()=="r":
        playGame()
    elif symbol.lower()=="q":
        root.destroy()

def runGame():
    global running
    running = False
    #Title and shadow
    screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#262525")
    screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#000000")

    screen.create_rectangle(25+155*1, 300, 155+155*1, 350, fill="#fff", outline="#111")
    screen.create_text(25+1*44+155*1.14,325,text="start", font=("Consolas",25),fill="#aaa")
    screen.update()

def drawGridBackground():
    cell_height = 500 / 8
    cell_width = 500 / 8
    # Draw the horizontal lines first
    for row in range(1, 8):
        screen.create_line(0, row * cell_width, 500, row * cell_width)
        screen.create_line(row * cell_height, 0, row * cell_height, 500)


def playGame():
    global board, running, alphabeta
    running = True
    screen.delete(ALL)
    # create_buttons()
    board = 0
    #Draw the background
    drawGridBackground()
    #Create the board and update it
    board = ReversiBoard(8)
    alphabeta = AlphaBeta(board)
    board.initBoard()
    board.update(screen,alphabeta)         

#When the user clicks, if it's a valid move, make the move
def clickHandle(event):
    global depth
    xMouse = event.x
    yMouse = event.y

    cell_height = 500 / 8
    cell_width = 500 / 8
    if running:
        if board.player==BLACK:
            pointx = event.x
            pointy = event.y
            y = int(pointy // cell_height)
            if y == 8:
                y -= 1
            x = int(pointx // cell_width)
            if x == 8:
                x -= 1
            moves = board.getLegalMoves(BLACK)
            
            for m in moves:
                col=int(board.point2position(m)[1])-1
                row=board.alpha2Row(board.point2position(m)[0])
                if(y==row and col == x):
                    board.makeMove(BLACK,m,screen,alphabeta)
    else:
        playGame()

runGame()

screen.bind("<Button-1>", clickHandle)
screen.bind("<Key>",keyHandle)
screen.focus_set()

#Run forever
root.wm_title("Othello")
root.mainloop()
