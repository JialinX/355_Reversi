from board import ReversiBoard

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
        board2d = self.board.boardTo2d()
        self.board.showBoard()
        
        for i in range(self.board.size):
            for j in range(self.board.size):
                if board2d[i][j] == color:
                    total += self.weight[i][j]
        print('heuristic',total)
        return total
    
    def genMove(self, color):
        move = self.alphabeta(color, 1)
        return move
    
    def alphabeta(self, color, depth):
        # alpha: best already explored option along path to the root for the maximizer
        # beta:  best already explored option along path to the root for the minimizer
        best = -9999
        moves = self.board.getAllLegalMoves(color)
        bestMove = moves[0]
        optColor = self.board.getOptColor(color)
        self.board.play(color, move)
        self.board.undo()
        print(color, optColor)    
        # for move in moves:
        #     self.board.play(color, move)
        #     #if this state is visited before 
        #     value = self.board.getHistory()
        #     print(value)
        #     if value == False:
        #         value = self.min_alphabeta(optColor, color, depth+1, -9999, 9999)
        #         self.board.addHistory(value)
                
        #     self.board.undo()
        #     if (value>best):
        #         best = value
        #         bestMove = move
                
        return bestMove
    
    def min_alphabeta(self, color, originalColor, depth, alpha, beta):
        print('min_',color,depth)
        localMin = 9999
        optColor = self.board.getOptColor(color)
        
        if depth == 2 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)
    
        moves = self.board.getAllLegalMoves(color)
        print(moves)
        for move in moves:
            print('deep:',depth, 'before play')
            self.board.showBoard()
            self.board.play(color, move)
            print('deep:',depth, 'after play')
            self.board.showBoard()
            value = self.board.getHistory()
            if value == False:
                value = self.max_alphabeta(optColor, originalColor, depth+1, alpha, beta)
                self.board.addHistory(value)
                
            self.board.undo()

            print('deep:',depth, 'after undo')            
            self.board.showBoard()
            if value < localMin:
                localMin = value
    
            if localMin <= alpha: #pruning
                return localMin
    
            beta = min(localMin, beta)
    
        return localMin
    
    def max_alphabeta(self, color, originalColor, depth, alpha, beta):
        print('max_',color,depth)
        localMax = -9999
        optColor = self.board.getOptColor(color)
        
        if depth == 2 or self.board.isEnd():
            return self.getHeuristicWeight(originalColor)
    
        moves = self.board.getAllLegalMoves(color)
        
        for move in moves:
            print('deep:',depth, 'before play')
            self.board.showBoard()
            self.board.play(color, move)
            print('deep:',depth, 'after play')            
            self.board.showBoard()
            value = self.board.getHistory()
            if value == False:                
                value  = self.min_alphabeta(optColor, originalColor, depth+1, alpha, beta)
                self.board.addHistory(value)
            
            self.board.undo()
            print('deep:',depth, 'after undo')
            self.board.showBoard()
            if value > localMax:
                localMax = value
    
            if localMax >= beta : #pruning
                return localMax
            
            alpha = max(localMax, alpha)
                
        return localMax

