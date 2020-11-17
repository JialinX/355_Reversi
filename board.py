import numpy as np

BLACK = 1 # player x 
WHITE = 2 # player o
EMPTY = 0

class ReversiBoard():

    def __init__(self, size):
        self.size = size
        self.startingBoard()
        
    def startingBoard(self):
        assert self.size%2==0
        mid = int(self.size/2)
        board2d = np.zeros((self.size, self.size))
        board2d[mid  ][mid  ] = 2
        board2d[mid-1][mid-1] = 2
        board2d[mid  ][mid-1] = 1
        board2d[mid-1][mid  ] = 1
        self.board1d = self.boardTo1d(board2d)

    def showBoard(self):
        pass

    def boardTo2d(self):
        board2d = np.reshape(b, (-1, self.size))
        return board2d

    def boardTo1d(self, board2d):
        board1d = board2d.flatten()
        return board1d

    def printMenu(self):
        print('  h            help menu')
        print('  x a2         play x a 2')
        print('  o g3         play o g 3')
        print('  . e3         erase e 3')
        print('  g x/o        genmove for x/o')
        print('  l x/o        show legal moves for x/o')
        print('  u            undo')

    def genMove(self, color):
        moves = getAllLegalMoves(color)
        pass

    def convertLetterPosition(self, position):
        letter = position[0]
        number = position[1]
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        return alphabet.index(letter)*self.size + number
    
    def getAllLegalMoves(self, color):
        optColor = 3 - color
        markBefore = self.getMark(optColor)
        legalMoves = []
        for position in self.board1d:
            if position == EMPTY: # to be changed to all adjcent cells instead of empty cells
                
                self.play(color, position)
                if self.getMark(optColor) != markBefore:
                    moves.append(position)
                self.undo()

        return legalMoves

    def erase(self, color, position):
        self.board1d[self.convertLetterPosition(position)] = 0

    def play(self, color, position):
        pass
    
    def getMark(self, color):
        mark = 0
        for i in self.board1d:
            if i == color:
                mark += 1
        return mark





    