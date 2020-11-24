import numpy as np
from copy import deepcopy
import random
BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.' # empty point
BORDER = '#' # border point

class ReversiBoard:

	def __init__(self,size):
		self.size = size
		self.currentPlayer = None
		self.computerColor = None
		self.humanColor = None
		self.currentPlayer = BLACK
		self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
		self.maxpoint = (self.size+2)*self.size + self.size
		self.minpoint = self.size+3
		self.NS = size + 2
		self.pass2 = 0
		self.directions=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
		self.boardHistory = []
		self.initBoard()

	def setBothColor(self, color):

		self.humanColor = color
		self.computerColor = WHITE if color == BLACK else BLACK

	def row_start(self, row):
		return row * self.NS + 1

	def initBoard(self):

		self.board = np.full(pow((self.size + 2),2), BORDER, dtype = 'U')
		for row in range(1, self.size + 1):
			start = self.row_start(row)
			self.board[start : start + self.size] = EMPTY
		self.board[44],self.board[55] = WHITE,WHITE
		self.board[45],self.board[54] = BLACK,BLACK

	def get_twoD_board(self):
		board2d = [[EMPTY for i in range(self.size)] for j in range(self.size)]
		for row in range(self.size):
			start = self.row_start(row + 1)
			board2d[row] = self.board[start : start + self.size]
		return board2d

	def showBoard(self):

		colString = " " + "".join([str(i).center(3) for i  in range(1,self.size+1)])
		board2d = self.get_twoD_board()
		print(colString)
		for row in range(self.size):
			strRow = [str(i).center(3) for i in board2d[row]]
			rowString =  str(self.alphabet[row]) + "".join(strRow)
			print(rowString)

	def position2point(self,position):

		letter, col = position
		assert letter in self.alphabet[:self.size]
		col = int(col)
		assert 1 <= col <= self.size
		row = self.alphabet.index(letter)
		assert 0 <= row <=  self.size - 1
		point = (row+1)*(self.size+2) + col
		assert self.minpoint <= point <= self.maxpoint
		return point

	def point2position(self,point):

		assert self.minpoint <= point <= self.maxpoint
		return self.alphabet[(point//(self.size+2)) - 1]+str(point % (self.size+2))

	def getScore(self, color):

		assert color in [BLACK, WHITE]
		score = 0
		for point in self.board:
			if point == color:
				score += 1
		return score

	def isPositionValid(self, position, color):

		assert color in [BLACK, WHITE]
		letter, col = position
		assert letter in self.alphabet[:self.size]
		j = int(col)
		assert 1 <= j <= self.size
		i = self.alphabet.index(letter) + 1
		for item in self.directions:
			i_step,j_step = item
			valid,end = self.valid_move(i+i_step,j+j_step,i_step,j_step,color)
			if valid:
				return True,end

		return False,None

	def valid_move(self,i,j,i_step,j_step,color):

		assert color in [BLACK, WHITE]
		point = i * (self.size+2) + j

		if self.board[point] in [EMPTY,BORDER,color]:
			return False,None
		else:
			return self.check_directions(i+i_step,j+j_step, i_step, j_step,color)

	def check_directions(self, i,j,i_step,j_step,color):

		assert color in [BLACK, WHITE]
		point = i * (self.size+2) + j
		if self.board[point] == color:
			return True, [i,j]
		elif self.board[point] in [EMPTY, BORDER]:
			return False, None

		return self.check_directions(i+i_step,j+j_step, i_step,j_step,color)

	def genMove(self,color):
		legalMoves = self.getLegalMoves(color)
		if legalMoves:
			return random.choice(legalMoves)
		return False


	def playMove(self, point,color):

		assert self.minpoint <= point <= self.maxpoint
		assert color in [BLACK, WHITE]

		position = self.point2position(point)
		if not self.isPositionValid(position, color):
			return False

		if self.board[point] == EMPTY:
			copyBoard = deepcopy(self.board)
			self.boardHistory.append(copyBoard)
			self.board[point] = color

		position = self.point2position(point)
		self.reverse_color(position,color)
		self.change_current_player()

	def undo(self):

		self.board = self.boardHistory.pop()

	def reverse_color(self, position, color):

		assert color in [BLACK, WHITE]
		letter, col = position
		assert letter in self.alphabet[:self.size]
		j = int(col)
		assert 1 <= j <= self.size
		i = self.alphabet.index(letter) + 1
		for item in self.directions:
			i_step,j_step = item
			valid,end = self.valid_move(i+i_step,j+j_step,i_step,j_step,color)
			if valid and end:
				self.start_reverse(i+i_step,j+j_step,i_step,j_step,color)

	def start_reverse(self,i,j,i_step,j_step,color):

		assert color in [BLACK, WHITE]
		point = i * (self.size+2) + j
		if self.board[point] == color:
			return
		self.board[point] = color
		self.start_reverse(i+i_step, j+j_step, i_step, j_step, color)


	def change_current_player(self):

		self.currentPlayer = BLACK if self.currentPlayer == WHITE else WHITE

	def getOptColor(self, color):

		return WHITE if color == BLACK else BLACK

	def getLegalMoves(self, color):

		assert color in [BLACK, WHITE]
		legalMoves = []
		for point in range(self.minpoint, self.maxpoint+1):
			if self.board[point] == EMPTY:
				position = self.point2position(point)

				valid, end = self.isPositionValid(position, color)
				if valid:
					legalMoves.append(point)

		return legalMoves

	def isEnd(self):

		return self.pass2 == 2

	def getWinner(self):

		blackScore = self.getScore(BLACK)
		whiteScore = self.getScore(WHITE)
		if blackScore > whiteScore:
			return BLACK
		elif blackScore == whiteScore:
			return 'Tie'
		else:
			return WHITE

