from __future__ import print_function
import numpy as np
from .KonaneLogic import Board
from Game import Game
import sys
sys.path.append('..')


class KonaneGame(Game):
    moves = []

    def __init__(self):
        self.width = 18
        self.height = 18

    def getInitBoard(self):
        board = Board()
        return np.array(board.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.width, self.height)

    def getActionSize(self):
        # return number of actions
        return self.width**4

    # Parses int hash created by x1 + y1*base + x2*(base**2) + y2*(base**3)
    def _int2move(self, action, base, num):
        move = [None]*num
        tmp = action
        for i in range(0, num):
            move[i] = tmp % base
            tmp -= move[i]
            tmp = tmp // base
        return move

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)
        move = self._int2move(action, self.width, 4)
        self.moves.extend([move])
        b.execute_move(move, player)
        # print(b.pieces)
        return (b.pieces, -1 * player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board()
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x1, y1, x2, y2 in legalMoves:
            valids[x1+y1*b.width+x2*b.width**2+y2*b.width**3] = 1
        # print(sum(valids))
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, if player 1 won, -1 if player 1 lost
        b = Board()
        b.pieces = np.copy(board)
        # TODO: More efficient way to check if there are still available moves?
        if player == 1:
            if len(b.get_legal_moves(player)) == 0:
                return -1
            elif len(b.get_legal_moves(-1 * player)) == 0:
                return 1
            else:
                return 0
        else:
            if len(b.get_legal_moves(player)) == 0:
                return 1
            elif len(b.get_legal_moves(-1 * player)) == 0:
                return -1
            else:
                return 0

    # Assumption 1: Konane has Canonical form similar to othello
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return board * player

    # Assumption 2: Konane has Symmetries similar to othello??
    # TODO: Figure this shit out
    def getSymmetries(self, board, pi):
        return [(board,pi)]

        # mirror, rotational
        # assert(len(pi) == self.getActionSize())  # 1 for pass
        # pi_board = np.reshape(pi[:-1], (self.width, self.height, self.width, self.height))
        # l = []

        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(board, i)
        #         newPi = np.rot90(pi_board, i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(newPi)
        #         l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        # return l

    def stringRepresentation(self, board):
        return board.tostring()

    # Num of moves current player can make minus num of moves other player can make
    def getScore(self, board, player):
        b = Board()
        b.pieces = np.copy(board)
        numMovesMe = len(b.get_legal_moves(player))
        numMovesOpp = len(b.get_legal_moves(-1 * player))
        return numMovesMe - numMovesOpp


# Pulled from konaneServer.py and edited
def display(board):
    b = Board()
    b.pieces = np.copy(board)
    boardToStr = '  '
    for i in range(0, b.width):
        boardToStr += (str(i%10) + ' ')
    boardToStr += '\n'
    inc = 0
    for row in b.pieces:
        rowToStr = ''
        for piece in row:
            if piece == 1:
                rowToStr += 'X'
            elif piece == -1:
                rowToStr += 'O'
            else:
                rowToStr += '.'
            rowToStr += ' '
        rowToStr += "\n"
        boardToStr += (str(inc%10) + ' ' + rowToStr)
        inc += 1
    return boardToStr
