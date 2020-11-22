from board import ReversiBoard

# heuristic
weight=[[100, -10, 11,  6,  6, 11, -10, 100],
        [-10, -20,  1,  2,  2,  1, -20, -10],
        [ 10,   1,  5,  4,  4,  5,   1,  10],
        [  6,   2,  4,  2,  2,  4,   2,   6],
        [  6,   2,  4,  2,  2,  4,   2,   6],
        [ 10,   1,  5,  4,  4,  5,   1,  10],
        [-10, -20,  1,  2,  2,  1, -20, -10],
        [100, -10, 11,  6,  6, 11, -10, 100]]

def getHeuristicWeight(board, color):
    total = 0
    for i in range(board.size):
        for j in range(board.size):
            if board[i][j] == color:
                total += weight[i][j]
    return total

def genMove(board, color):
    move = alphabeta(color, depth)
    return move

def alphabeta(board, color, depth):
    # alpha: best already explored option along path to the root for the maximizer
    # beta:  best already explored option along path to the root for the minimizer
    best = -9999
    bestMove = None
    moves = board.getAllLegalMoves(color)

    for move in moves:
        board.play(color, move)
        value = board.getHistory()
        if value == False:
            value = min_alphabeta(board, 3-color, color, depth+1, -9999, 9999)
            board.addHistory(value)
        board.undo()

        if (value>best):
            best = value
            bestMove = move
            
    return move

def min_alphabeta(board, color, originalColor, depth, alpha, beta):
    localMin = 9999

    if depth == 5 or board.isEnd():
        return getHeuristicWeight(originalColor)

    moves = board.getAllLegalMoves(color)
    
    for move in moves:
        board.play(color)
        value  = max_alphabeta(board, 3-color, originalColor, depth+1, alpha, beta)
        board.undo()

        if value < localMin:
            localMin = value

        if localMin <= alpha: #pruning
            return localMin

        beta = min(localMin, beta)

    return localMin

def max_alphabeta(board, color, originalColor, depth, alpha, beta):
    localMax = -9999

    if depth == 5 or board.isEnd():
        return getHeuristicWeight(originalColor)

    moves = board.getAllLegalMoves(color)
    
    for move in moves:
        board.play(color)
        value  = min_alphabeta(board, 3-color, originalColor, depth+1, alpha, beta)
        board.undo()

        if value > localMax:
            localMax = value

        if localMax >= beta : #pruning
            return localMax
        
        alpha = max(localMax, alpha)
            
    return localMax


def main():
    board = ReversiBoard(8)
    while True:
        option = input()

if __name__ == '__main__':
    main()
