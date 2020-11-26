from board import ReversiBoard
from reversi import AlphaBeta
BLACK = 'x' # player black
WHITE = 'o' # player white

def pvpGame(board,alphabeta):

	"""
	pvpGame. used to play game between human
	:param board: list. Indicate current board state
	:param alphabeta: AlphaBeta. alphabeta instance
	:return: none
	"""

	board.showBoard()
	print("x goes first, o goes second")

	playerAColor = input("What color do you want to use? (x/o): ")
	while playerAColor[0].lower() not in [BLACK,WHITE,'w','b']:
		playerAColor = input("Invalid, input, please input again: ")
	board.setBothColor(playerAColor)
	playerBColor = board.getOptColor(playerAColor)
	print(f"PlayerA plays {playerAColor}, PlayerB plays {playerBColor}")

	while not board.isEnd():
		print(f"Current turn is {board.currentPlayer}")
		command = input("Commands>> ")
		if not command: continue
		dealCommand(command, board, alphabeta,board.currentPlayer, 'pvp')

	printResult(board)

def pvcGame(board,alphabeta):

	"""
	pvcGame. used to play game between human and computer
	:param board: list. Indicate current board state
	:param alphabeta: AlphaBeta. alphabeta instance
	:return: none
	"""

	board.showBoard()
	print("x goes first, o goes second")
	humanColor = input("What color do you want to use? (x/o): ")
	while humanColor[0].lower() not in [BLACK,WHITE,'w','b']:
		humanColor = input("Invalid, input, please input again: ")
	board.setBothColor(humanColor)
	if humanColor == WHITE:
		_, comMove = alphabeta.genMove(board.computerColor)
		board.playMove(comMove, BLACK)
		print(f"Computer played at {board.point2position(comMove)}")
		board.showBoard()

	while not board.isEnd():
		command = input("Commands>> ")
		if not command: continue
		dealCommand(command, board, alphabeta,humanColor, 'pvc')

	printResult(board)

def showLegalMove(board, color):
	"""
	showLegalMove. To show legal moves for the current player
	:param board: list. Indicate current board state
	:param color: str. Indicate current player's color
	:return: none
	"""
	moves = board.getLegalMoves(color)
	if not moves:
		print("You have no legal moves, enter 'p' to pass your turn")
		return
	else:
		allMoves = " ".join([board.point2position(move) for move in moves])
		print(f"All legal moves for {color} are: {allMoves}")

def printResult(board):
	"""
	printResult. Print the result of a given board state
	:return: none
	"""
	print(f"The game winner is {board.getWinner()}")
	print(f"{BLACK} has score {board.getScore(BLACK)}")
	print(f"{WHITE} has score {board.getScore(WHITE)}")

def humanPlayMove(board,point, humanColor):

	"""
	printResult. Print the result of a given board state
	:param board: str. Indicate player's input
	:param point: int. Indicate a move from the player
	:param humanColor: str. Indicate player's color
	:return: False if error happenes, True if move is placed on the board
	"""

	moves = board.getLegalMoves(humanColor)
	if not moves:
		print(f"There is no legal moves for {humanColor}, you have to input 'p' to pass your turn")
		return False

	if point in moves:
		board.playMove(point, humanColor)
		print(f"{humanColor} played at {board.point2position(point)}")
		board.pass2 = 0
		board.showBoard()
		return True
	else:
		print(f"Invalid position for {humanColor}, please select from following moves")
		showLegalMove(board, humanColor)
		return False

def computerPlayMove(board, alphabeta, computerColor):

	"""
	printResult. Print the result of a given board state
	:param board: str. Indicate player's input
	:param alphabeta: AlphaBeta. alphabeta instance
	:param computerColor: str. Indicate computer's color
	:return: none
	"""

	_, move = alphabeta.genMove(computerColor)
	if move is None:
		board.pass2 += 1
		board.change_current_player()
		print("Computer has no legal moves, it passed current turn")
	else:
		board.playMove(move,computerColor)
		board.pass2 = 0
		print(f"Computer played at {board.point2position(move)}")
		board.showBoard()

def dealCommand(commands, board, alphabeta, humanColor, mode):

	"""
	dealCommand. To present the corresponding commend from the player
	:param commands: str. Indicate player's input
	:param board: list. Indicate current board state
	:param alphabeta: class. Indicate alphabeta class
	:param humanColor: str. Indicate the player's color
	:param mode: str. Indicate the mode either be 'pvc' or 'pvp'
	:return: none
	"""
	commandLen = len(commands.split())

	if commands[0] == 'h':
		printMenu()

	elif commands[0] == 'b':
		board.showBoard()

	elif commands[0] in [BLACK, WHITE]:
		if commandLen != 2:
			print("Invalid command, please input again")
			return
		color, position = commands.split()
		if color != board.currentPlayer:
			print("You cannot play opponent's color")
			return
		if len(position) != 2:
			print("Invalid command, please input again")
			return
		letter, col = position
		if letter not in board.alphabet[:board.size] or \
			not col.isdigit() or int(col) not in range(1,board.size+1):
			print("Invalid position, please input again")
			return

		point = board.position2point(position)
		success = humanPlayMove(board, point, humanColor)
		if success and mode == 'pvc':
			computerPlayMove(board, alphabeta, board.computerColor)
		else:
			return

	elif commands[0] == 'g':
		if commandLen != 2:
			print("Invalid command, please input again.")
			return
		_, color = commands.split()
		_, move = alphabeta.genMove(color)
		if move is not None:
			print(f"The best move found by AlphaBeta is {board.point2position(move)}")
		else:
			print("There are no move generated by Alphabeta")
			return

	elif commands[0] == 'l':
		if commandLen != 2:
			print("Invalid command, please input again")
			return
		_, color = commands.split()
		if color.lower() not in [BLACK,WHITE]:
			print("Invalid color, please input again")
			return
		showLegalMove(board, color)

	elif commands[0] == 'u':
		if not board.boardHistory:
			print("There is no move to undo")
			return
		board.undo()
		board.showBoard()

	elif commands[0] == 'p':
		board.pass2 += 1
		board.change_current_player()
		print("You have passed your current turn, it's your opponent's turn now")
		if mode == 'pvc':
			computerPlayMove(board, alphabeta, board.computerColor)

	elif commands[0] == 'q':
		print("Bye ...")
		board.end = True

	else:
		print("Invalid command, please input again")
		return

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

def main():

	board = ReversiBoard(8)
	alphabeta = AlphaBeta(board)
	print("Do you wanna play against computer? (y/n)")
	print("If y(es), computer will play with you")
	print("If n(o), the board is just for testing or pvp use")
	pvp = input(">> ")
	while pvp[0].lower() not in ['y','n']:
		print("Invalid input, please enter again")
		pvp = input(">> ")
	if pvp[0].lower() == 'y':
		pvcGame(board,alphabeta)
	else:
		pvpGame(board,alphabeta)

main()

