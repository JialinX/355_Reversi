class AlphaBeta:
    def __init__(self, board):
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

        total = 0
        board2d = self.board.get_twoD_board()
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board2d[i][j] == color:
                    total += self.weight[i][j]
        return total

    def genMove(self, color):

        return self.alphabeta(color, 1)

    def alphabeta(self, color, depth):
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

