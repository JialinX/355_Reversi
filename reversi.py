class AlphaBeta:
    def __init__(self, board):
        """
        __init__. To initialize class data board and heuristic lists.
        :param board: list. Indicate the given board structure 
        """
        self.board = board
        self.weight=[[100, -10, 11,  6,  6, 11, -10, 100],
                    [-10, -20,  1,  2,  2,  1, -20, -10],
                    [ 10,   1,  5,  4,  4,  5,   1,  10],
                    [  6,   2,  4,  2,  2,  4,   2,   6],
                    [  6,   2,  4,  2,  2,  4,   2,   6],
                    [ 10,   1,  5,  4,  4,  5,   1,  10],
                    [-10, -20,  1,  2,  2,  1, -20, -10],
                    [100, -10, 11,  6,  6, 11, -10, 100]]

    def getHeuristicWeight(self, color):
        """
        getHeuristicWeight. To obtain the total heuristic of the given player
        :param color: int. Indicate the given player's color
        :return: int. Return the accumulated heuristic of the given player
        """
        total = 0
        board2d = self.board.get_twoD_board()
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board2d[i][j] == color:
                    total += self.weight[i][j]
        return total

    def genMove(self, color):
        """
        genMove. To generate the optimal next move for the given player's color
        :param color: int. Indicate the given player's color
        :return: list. Indicate next optimal move for the given player's color
        """
        return self.alphabeta(color, 1)

    def alphabeta(self, color, depth):
        """
        alphabeta. To start the minimax search with pruning by traversing the legal move list
        to find the optimal move with maximal score
        :param color: int. Indicate the given player's color
        :param depth: int. Indicate the search depth for alpha_beta search
        :return: (int,list). Indicate next optimal score and move for the given player's color
        """
        import time
        #time.sleep(3)
        best = -9999
        moves = self.board.getLegalMoves(color)
        if len(moves) == 0:
            return 0, None

        bestMove = moves[0]
        optColor = self.board.getOptColor(color)

        for move in moves:
            self.board.playMove(move, color)
            value = self.min_alphabeta(optColor, color, depth+1, -9999, -9999)
            self.board.undo()

            if value > best:
                best = value
                bestMove = move

        return best,bestMove

    def min_alphabeta(self, color, originalColor, depth, alpha, beta):
        """
        min_alphabeta. To obtain the minimal score for the maximizer by traversing the legal move list within
        the specified depth
        :param color: int. Indicate the opponent player's color
        :param originalColor: int. Indicate the given player's color
        :param depth: int. Indicate the search depth for alpha_beta search
        :param alpha: int. Indicate current score for alpha
        :param beta: int. Indicate current score for beta
        :return: int. Return current local minimal score for beta
        """
        localMin = 9999
        optColor = self.board.getOptColor(color)

        if depth == 5 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)

        moves = self.board.getLegalMoves(color)
        if len(moves) == 0:
            return localMin

        for move in moves:
            self.board.playMove(move, color)
            value = self.max_alphabeta(optColor, originalColor,depth+1,alpha,beta)
            self.board.undo()

            if value < localMin:
                localMin = value

            if localMin <= alpha:
                return localMin

            beta = min(localMin, beta)

        return localMin

    def max_alphabeta(self, color, originalColor, depth, alpha, beta):
        """
        max_alphabeta. To obtain the maximal score for the minimizer by traversing the legal move list within
        the specified depth
        :param color: int. Indicate the opponent player's color
        :param originalColor: int. Indicate the given player's color
        :param depth: int. Indicate the search depth for alpha_beta search
        :param alpha: int. Indicate current score for alpha
        :param beta: int. Indicate current score for beta
        :return: int. Return current local maximal score for alpha
        """
        localMax = -9999
        optColor = self.board.getOptColor(color)

        if depth == 5 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)

        moves = self.board.getLegalMoves(color)
        if len(moves) == 0:
            return localMax

        for move in moves:
            self.board.playMove(move,color)
            value = self.min_alphabeta(optColor, originalColor,depth+1, alpha, beta)
            self.board.undo()

            if value > localMax:
                localMax = value

            if localMax >= beta:
                return localMax

            alpha  = max(localMax, alpha)

        return localMax

