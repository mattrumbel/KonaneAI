from flask import Flask
from datetime import datetime
from random import seed, randint
import sys
import math

app = Flask(__name__)

boardWidth = 18
boardHeight = 18
playerPiece = ('b','w')
emptyPiece = 0

startingPieces = [(0,0), (0, boardWidth - 1), (boardHeight - 1, boardWidth - 1), (boardHeight - 1, 0), (boardHeight//2 - 1, boardWidth//2 - 1), (boardHeight//2 - 1, boardWidth//2), (boardHeight//2, boardWidth//2), (boardHeight//2, boardWidth//2 - 1)]

startSurround = [(-1,0), (0, 1), (1, 0), (0, -1)]

board = [[playerPiece[(i+j) % 2] for j in range(0, boardWidth)] for i in range(0, boardHeight)]

seed(datetime.now())
playerID = (randint(0, 2000), randint(0,2000))
while playerID[0] == playerID[1]:
        playerID = (randint(0, 2000), randint(0,2000))

joined = [False, False]
gotID = [False, False]
currentPlayer = 0  
startPiece = (0,0)

def nextPlayer():
    global currentPlayer
    currentPlayer = (currentPlayer + 1) % 2

@app.route("/")
def helloWorld():
    return "Hello World"

@app.route("/getBoardVal/<xLoc>/<yLoc>")
def getBoardVal(xLoc, yLoc):
    xLoc = int(xLoc)
    yLoc = int(yLoc)
    return board[yLoc][xLoc]

@app.route("/getPlayerColor/<pNum>")
def getPlayerColor(pNum):
    pNum = int(pNum)
    return playerPiece[pNum]

@app.route("/join")
def join():
    if not (joined[0] and joined[1]):
        if not joined[0] and not joined[1]:
            rand = randint(0,1)
            joined[rand] = True
            return str(rand)
        else:
            print("LETS START THE GAME!!!")
            if not joined[0]:
                joined[0] = True
                return str(0)
            else:
                joined[1] = True
                return str(1)
    else:
        return "Two players are already playing"

@app.route("/getPlayerID/<pNum>")
def getPlayerID(pNum):
    pNum = int(pNum)
    if not gotID[pNum]:
        gotID[pNum] = True
        return str(playerID[pNum])
    else:
        return "ID already taken"

@app.route("/currentPlayer")
def getCurrentPlayer():
    return str(currentPlayer)

@app.route("/printBoard")
def printBoard():
    boardToStr = '  '
    for i in range(0, boardWidth):
        boardToStr += (str(i%10) + ' ')
    boardToStr += '\n'
    inc = 0
    for row in board:
        rowToStr = ' '.join(map(str, row)) + "\n"
        boardToStr += (str(inc%10) + ' ' + rowToStr)
        inc += 1
    return boardToStr

@app.route("/isFirstValid/<xLoc>/<yLoc>")
def isFirstValid(xLoc, yLoc):
    xLoc = int(xLoc)
    yLoc = int(yLoc)
    for i in range(len(startingPieces)):
        if startingPieces[i][0]==yLoc and startingPieces[i][1]==xLoc:
            startPiece = (xLoc, yLoc)
            return 'True'
    return 'False'

@app.route("/isSecondValid/<pNum>/<xLoc>/<yLoc>")
def isSecondValid(pNum, xLoc,yLoc):
    pNum = int(pNum)
    xLoc = int(xLoc)
    yLoc = int(yLoc)
    if xLoc>boardWidth or yLoc>boardHeight or xLoc<0 or yLoc<0 or board[yLoc][xLoc]!=playerPiece[pNum]:
        return 'False'
    for i in range(len(startSurround)):
        newX = startPiece[0] + startSurround[i][0]
        newY = startPiece[1] + startSurround[i][1]
        if xLoc==newX and yLoc==newY:
            return 'True'
    return 'False'

@app.route("/isMoveValid/<pNum>/<startX>/<startY>/<endX>/<endY>")
def isMoveValid(pNum, startX, startY, endX, endY):
    pNum = int(pNum)
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    dirX = 0
    dirY = 0
    if endX - startX > 0:
        dirX = 1
    elif endX - startX < 0:
        dirX = -1
    if endY - startY > 0:
        dirY = 1
    elif endY - startY < 0:
        dirY = -1

    if pNum==currentPlayer:
        if startX < boardWidth and startY < boardHeight and endX < boardWidth and endY < boardHeight and startX >= 0 and startY >= 0 and endX >= 0 and endY >= 0:
            if (startX == endX and not startY == endY) or (not startX == endX and startY == endY):
                if board[startY][startX] == playerPiece[currentPlayer]:
                    if board[endY][endX] == emptyPiece and endY % 2 == startY % 2 and endX % 2 == startX % 2:
                        if startX == endX:
                            for i in range(min(startY, endY), max(startY, endY), 2):
                                if board[i + dirY][startX] == playerPiece[currentPlayer] or board[i + dirY][startX] == emptyPiece:
                                    return 'False'
                            return 'True'
                        elif startY == endY:
                            for i in range(min(startX, endX), max(startX, endX), 2):
                                if board[startY][i + dirX] == playerPiece[currentPlayer] or board[startY][i + dirX] == emptyPiece:
                                    return 'False'
                            return 'True'
    return 'False'

@app.route("/removeStartPiece/<pNum>/<xLoc>/<yLoc>")
def removeStartPiece(pNum, xLoc, yLoc):
    xLoc = int(xLoc)
    yLoc = int(yLoc)
    pNum = int(pNum)
    global playerPiece
    global startPiece

    if(pNum == 0):
        if board[yLoc][xLoc]=='b':
            playerPiece = ('b','w')
        else:
            playerPiece = ('w', 'b')
    board[yLoc][xLoc] = emptyPiece
    nextPlayer()
    return printBoard()

@app.route("/move/<startX>/<startY>/<endX>/<endY>")
def move(startX, startY, endX, endY):
    print(playerPiece)
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    dirX = 0
    dirY = 0
    if endX - startX > 0:
        dirX = 1
    elif endX - startX < 0:
        dirX = -1
    if endY - startY > 0:
        dirY = 1
    elif endY - startY < 0:
        dirY = -1

    if startX == endX:
        board[startY][startX] = emptyPiece
        for i in range(min(startY, endY), max(startY, endY), 2):
            board[i + dirY][startX] = emptyPiece
    else:
        board[startY][startX] = emptyPiece
        for i in range(min(startX, endX), max(startX, endX), 2):
            board[startY][i + dirX] = emptyPiece

    board[endY][endX] = playerPiece[currentPlayer]
    nextPlayer()
    return printBoard()

if __name__ == "__main__":
    print("Running Main")
    app.run(host="0.0.0.0")
