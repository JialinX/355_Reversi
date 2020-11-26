import matplotlib.pyplot as plt
from board import ReversiBoard
from reversi import AlphaBeta
from copy import deepcopy

BLACK = 'x' # player black
WHITE = 'o' # player white
EMPTY = '.'
BORDER = '#'

humanColor = BLACK
computerColor = WHITE


total = 10
avgAlpha = []
avgGree = []
avgRandom = []
totalepisode = 100

def greedy(board):
    """
    greedy. To implement greedy algorithm to search for the next best move
    :param board: list. Indicate the current board state
    :return: list. Containing score for both players
    """
	alphabeta = AlphaBeta(board)

	while not board.isEnd():
				
		moves = board.getLegalMoves(humanColor)
		if not moves and board.pass2 == 1:
			break
		elif not moves and board.pass2 == 0:
			board.pass2 += 1
		elif len(moves) > 0:
			board.pass2 = 0
			move = board.genGreedyMove(humanColor)
			board.playMove(move, humanColor)
		_, comMove = alphabeta.genMove(computerColor)
		if not comMove and board.pass2 == 1:
			break
		elif not comMove and board.pass2 == 0:
			board.pass2 += 1
		elif comMove != None:
			board.pass2 = 0
			board.playMove(comMove, computerColor)
	blackScore = board.getScore(BLACK)
	whiteScore = board.getScore(WHITE)

	return whiteScore,blackScore

def random(board):
    """
    random. To implement random algorithm to search for the next move
    :param board: list. Indicate the current board state
    :return: list. Containing score for both players
    """
	alphabeta = AlphaBeta(board)

	while not board.isEnd():
				
		moves = board.getLegalMoves(humanColor)
		if not moves and board.pass2 == 1:
			break
		elif not moves and board.pass2 == 0:
			board.pass2 += 1
		elif len(moves) > 0:
			board.pass2 = 0
			move = board.genMove(humanColor)
			board.playMove(move, humanColor)
		_, comMove = alphabeta.genMove(computerColor)
		if not comMove and board.pass2 == 1:
			break
		elif not comMove and board.pass2 == 0:
			board.pass2 += 1
		elif comMove != None:
			board.pass2 = 0
			board.playMove(comMove, computerColor)
	blackScore = board.getScore(BLACK)
	whiteScore = board.getScore(WHITE)
	
	return whiteScore,blackScore

def main():
	alphaScores = []
	greeScores = []
	randScores = []
	for j in range(totalepisode):
		#boardA = ReversiBoard(8)
		boardB = ReversiBoard(8)
		#boardA.setBothColor(humanColor)
		boardB.setBothColor(humanColor)
		#alpha_greedy_score, gree_score = greedy(boardA)
		alpha_random_score, rand_score = random(boardB)
		alphaScores.append(alpha_random_score)
		#greeScores.append(gree_score)
		randScores.append(rand_score)

	episodeList = list(range(1,totalepisode + 1))

	fig,ax=plt.subplots(figsize=(10,5))
	ax.plot(episodeList,alphaScores,'-',color='xkcd:azure',label="AlphaBeta Player")
	#ax.plot(episodeList,greeScores,'-',color='limegreen', label="Greedy Player")
	ax.plot(episodeList,randScores,'-',color='gray', label="Random Player")
	leg = ax.legend();
	ax.set_ylabel("\nScore",fontsize=16,fontweight='bold',rotation=0)
	ax.set_xlabel("Game",fontsize=16,fontweight='bold')
	plt.yticks([0,8,16,24,32,40,48,56,64],fontsize=13)
	plt.xticks([1,10,20,30,40,50,60,70,80,90,100],fontsize=13)
	ax.yaxis.set_label_coords(-0.09,0.45)
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	plt.savefig("win.png")


main()