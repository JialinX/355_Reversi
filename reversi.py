#from board import ReversiBoard

class AlphaBetaGenMove:
    
    def __init__(self, board):
        # heuristic
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
<<<<<<< HEAD
        board2d = self.board.boardTo2d(self.board.board)
        #self.board.showBoard()
=======
        board2d = self.board.boardTo2d()
>>>>>>> da460cd79e2215c1941f88bd3ec557732f115daf
        
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board2d[i][j] == color:
                    total += self.weight[i][j]
        return total
    
    def genMove(self, color):
        move = self.alphabeta(color, 1)
        return move
    
    def alphabeta(self, color, depth):
        print("alphaBeta")
        # alpha: best already explored option along path to the root for the maximizer
        # beta:  best already explored option along path to the root for the minimizer
        best = -9999
        moves = self.board.getAllLegalMoves(color)
        if not moves:
            return (0, None)
        bestMove = moves[0]
        optColor = self.board.getOptColor(color)
 
        for move in moves:
            self.board.play(color, move)
            #if this state is visited before 
            value = self.board.getHistory()
            if value == False:
                value = self.min_alphabeta(optColor, color, depth+1, -9999, 9999)
                self.board.addHistory(value)
                
            self.board.undo()
            if (value>best):
                best = value
                bestMove = move
                
        return (best,bestMove)
    
    def min_alphabeta(self, color, originalColor, depth, alpha, beta):
        localMin = 9999
        optColor = self.board.getOptColor(color)
        
        if depth == 5 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)
    
        moves = self.board.getAllLegalMoves(color)
        
        for move in moves:
            self.board.play(color, move)
            value = self.board.getHistory()
            if value == False:
                value = self.max_alphabeta(optColor, originalColor, depth+1, alpha, beta)
                self.board.addHistory(value)
                
            self.board.undo()
           
            if value < localMin:
                localMin = value
    
            if localMin <= alpha: #pruning
                return localMin
    
            beta = min(localMin, beta)
    
        return localMin
    
    def max_alphabeta(self, color, originalColor, depth, alpha, beta):
        localMax = -9999
        optColor = self.board.getOptColor(color)
        
        if depth == 5 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)
    
        moves = self.board.getAllLegalMoves(color)
        
        for move in moves:
            self.board.play(color, move)     
            value = self.board.getHistory()
            if value == False:                
                value  = self.min_alphabeta(optColor, originalColor, depth+1, alpha, beta)
                self.board.addHistory(value)
            
            self.board.undo()
            if value > localMax:
                localMax = value
    
            if localMax >= beta : #pruning
                return localMax
            
            alpha = max(localMax, alpha)
                
        return localMax

