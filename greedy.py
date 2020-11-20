from board import ReversiBoard
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
    for point in range(len(board.board)):
        position = board.point2position(point)
        if board.board[point]== color:
            total += weight[position[0]][position[1]]
    return total


def greedy(board, color):
    best = -9999
    bestMove = None
    moves = board.getAllLegalMoves(color)
    for move in moves:
        board.play(color, move)
        value = getHeuristicWeight(board, color)
        board.erase(move)
        if (value > best):
            best = value
            bestMove = move
            
    return move