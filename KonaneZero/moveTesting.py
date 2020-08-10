from konane.KonaneGame import KonaneGame as Game
from konane.KonaneGame import display
from konane.KonaneLogic import Board
import numpy as np
from MCTS import MCTS
from konane.pytorch.NNet import NNetWrapper as nn
from utils import *
from Coach import Coach

errorBoard = [[1,-1,1,-1,1,0,0,-1,0,0,0,0,0,-1,0,0,0,-1],
              [-1,0,0,0,0,0,0,0,0,0,0,0,-1,0,-1,0,0,1],
              [1,0,0,0,0,0,0,0,0,-1,0,0,0,-1,0,0,0,0],
              [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,1,0,1,0,1,0,0,-1,0,0,0,-1],
              [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,0,1,0,0,-1,0,0,0,0,1,0,1,-1],
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
              [0,0,0,0,0,-1,0,0,1,0,0,0,0,0,1,0,0,0],
              [0,0,-1,0,0,0,-1,0,0,1,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0],
              [0,0,0,0,0,0,-1,0,0,0,0,0,0,1,0,1,0,1],
              [1,0,0,0,1,0,0,0,0,0,0,-1,0,0,0,0,1,0],
              [0,0,-1,0,0,1,0,0,-1,0,0,0,-1,0,-1,0,0,0],
              [1,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0],
              [0,0,-1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
              [1,0,0,0,0,-1,0,0,0,0,0,0,1,0,0,0,0,0],
              [0,0,0,0,0,0,0,1,0,1,0,1,0,0,-1,0,0,1]]
# for i in errorBoard:
#     if len(i) != 18:
#         print("Oh you fucked up on line ", i)

board = Board()
board.pieces = errorBoard
print("Here is the current board:")
print(display(board.pieces))
# print("Here are all of the legal moves you can make: ", board._getValidMoves(-1))

# args = dotdict({
#         'numIters': 100,
#         'numEps': 10,
#         'tempThreshold': 5,
#         'updateThreshold': 0.6,
#         'maxlenOfQueue': 200000,
#         'numMCTSSims': 4,
#         'arenaCompare': 40,
#         'cpuct': 1,

#         'checkpoint': './temp/',
#         'load_model': False,
#         'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
#         'numItersForTrainExamplesHistory': 20,})

# game = Game()
# nnet = nn(game)
# myCoach = Coach(game, nnet, args)
# color = -1

# canonicalBoard = myCoach.game.getCanonicalForm(np.array(errorBoard), color)
# pi = myCoach.mcts.getActionProb(canonicalBoard)
# for i in range(len(pi)):
#     if pi[i] != 0:
#         print("At position: ", i, " we have value: ", pi[i])
# action = np.random.choice(len(pi), p=pi)
# move = myCoach.game._int2move(action, board.width, 4)
# print("This is your chosen move: ", move)

board = Board()
board.pieces = errorBoard
print("I found this many moveable pieces: ", board._getMoveablePieces(1))